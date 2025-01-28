import sys
import os
# ------------------------------------------------------------------------------------------------------------

import certifi
import litellm
litellm.set_verbose = True  # Enable detailed debugging
# Set SSL certificate path explicitly
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
litellm.drop_params = True  # Clear existing params
litellm.ssl_verify = False  # Disable SSL verification (not recommended for production)

#



from flask import Flask, Response, jsonify
from threading import Thread
from queue import Queue
import sys
import json
import time
import os

# Add the src directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.config_loader import ConfigLoader
from src.llm_setup import LLMSetup
from src.crew_setup import CrewSetup
from src.models import ProjectPlan

app = Flask(__name__)

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

def run_crew(inputs, output_capturer):
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
    finally:
        sys.stdout = original_stdout

@app.route('/stream')
def stream():
    output_capturer = OutputCapturer()
    
    project_data = {
        'project': 'Website',
        'industry': 'Technology',
        'project_objectives': 'Create a website for a small business',
        'team_members': """
            - John Doe (Project Manager)
            - Jane Doe (Software Engineer)
            - Bob Smith (Designer)
            - Alice Johnson (QA Engineer)
            - Tom Brown (QA Engineer)
            """,
        'project_requirements': """
            - Create a responsive design that works well on desktop and mobile devices
            - Implement a modern, visually appealing user interface with a clean look
            - Develop a user-friendly navigation system with intuitive menu structure
            - Include an "About Us" page highlighting the company's history and values
            - Design a "Services" page showcasing the business's offerings with descriptions
            - Create a "Contact Us" page with a form and integrated map for communication
            - Implement a blog section for sharing industry news and company updates
            - Ensure fast loading times and optimize for search engines (SEO)
            - Integrate social media links and sharing capabilities
            - Include a testimonials section to showcase customer feedback and build trust
            """
    }

    inputs = {
        'project_type': project_data['project'],
        'project_objectives': project_data['project_objectives'],
        'industry': project_data['industry'],
        'team_members': project_data['team_members'],
        'project_requirements': project_data['project_requirements']
    }

    thread = Thread(target=run_crew, args=(inputs, output_capturer))
    thread.start()

    def generate():
        while True:
            if not output_capturer.queue.empty():
                item_type, content = output_capturer.queue.get()
                if item_type == 'log':
                    yield f"data: {json.dumps({'type': 'log', 'data': content})}\n\n"
                elif item_type == 'result':
                    if isinstance(content, ProjectPlan):
                        content = content.dict()
                    yield f"data: {json.dumps({'type': 'result', 'data': content})}\n\n"
                    break
            else:
                if not thread.is_alive():
                    break
                time.sleep(0.1)
        thread.join()

    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)