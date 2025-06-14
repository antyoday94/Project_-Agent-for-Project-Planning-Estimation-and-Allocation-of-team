# File: FastAPI.py
import os
import sys
import json
import asyncio
from queue import Queue
from threading import Thread
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# LiteLLM configuration
import certifi
import litellm
os.environ['LITELLM_LOG'] = 'DEBUG'  # Updated verbose setting
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
litellm.drop_params = True
litellm.ssl_verify = False

# Add backend directory to path to allow "from src import..."
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config_loader import ConfigLoader
from src.llm_setup import LLMSetup
from src.crew_setup import CrewSetup
from src.models import ProjectPlan

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OutputCapturer:
    def __init__(self):
        self.queue = Queue()
        self.buffer = ''
        
    def write(self, data):
        self.buffer += data
        while '\n' in self.buffer:
            line, self.buffer = self.buffer.split('\n', 1)
            self.queue.put(('log', line.strip()))
            
    def flush(self):
        if self.buffer:
            self.queue.put(('log', self.buffer.strip()))
            self.buffer = ''

class ProjectInput(BaseModel):
    project: str
    industry: str
    project_objectives: str
    team_members: str
    project_requirements: str

def run_crew(inputs: dict, output_capturer: OutputCapturer):
    original_stdout = sys.stdout
    sys.stdout = output_capturer
    try:
        config_loader = ConfigLoader()
        configs = config_loader.load_configs()
        llm = LLMSetup.get_llm()
        crew_setup = CrewSetup(configs['agents'], configs['tasks'], llm)
        agents = crew_setup.create_agents()
        tasks = crew_setup.create_tasks(agents)
        crew = crew_setup.assemble_crew(agents, tasks)
        result = crew.kickoff(inputs=inputs)
        sys.stdout.flush()
        output_capturer.queue.put(('result', result))
    except Exception as e:
        output_capturer.queue.put(('error', str(e)))
    finally:
        sys.stdout = original_stdout

async def event_generator(output_capturer: OutputCapturer, thread: Thread):
    try:
        while True:
            if not output_capturer.queue.empty():
                item_type, content = output_capturer.queue.get()
                if item_type == 'log':
                    yield f"data: {json.dumps({'type': 'log', 'data': content})}\n\n"
                elif item_type == 'result':
                    # Handle different output types
                    if isinstance(content, BaseModel):  # For Pydantic models
                        content = content.dict()
                    elif hasattr(content, 'to_dict'):  # For custom objects with to_dict()
                        content = content.to_dict()
                    yield f"data: {json.dumps({'type': 'result', 'data': content})}\n\n"
                    break
                elif item_type == 'error':
                    yield f"data: {json.dumps({'type': 'error', 'data': content})}\n\n"
                    break
            else:
                if not thread.is_alive():
                    break
                await asyncio.sleep(0.1)
    finally:
        thread.join()

@app.post("/stream")
async def stream_crew(input_data: ProjectInput):
    output_capturer = OutputCapturer()
    
    inputs = {
        'project_type': input_data.project,
        'project_objectives': input_data.project_objectives,
        'industry': input_data.industry,
        'team_members': input_data.team_members,
        'project_requirements': input_data.project_requirements
    }

    thread = Thread(target=run_crew, args=(inputs, output_capturer))
    thread.start()

    return StreamingResponse(
        event_generator(output_capturer, thread),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
