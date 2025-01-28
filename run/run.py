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

# ------------------------------------------------------------------------------------------------------------

# import os
# import certifi
# import litellm
# from dotenv import load_dotenv

# # 1. Configure environment
# load_dotenv()
# os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
# os.environ['LITELLM_LOG'] = 'DEBUG'  # Enable detailed debugging
# # 2. Configure LiteLLM

# litellm.set_verbose = True
# litellm.telemetry = False  # Disable unnecessary data collection

# # 3. Test connection
# try:
#     response = litellm.completion(
#         model="gemini/gemini-pro",
#         messages=[{"role": "user", "content": "Hello"}],
#         ssl_verify=True  # Keep True for security
#     )
#     print(response)
# except Exception as e:
#     print(f"Error Details:\n{type(e).__name__}: {str(e)}")
#     if hasattr(e, 'llm_provider'):
#         print(f"Provider Error Code: {e.llm_provider}")


# ------------------------------------------------------------------------------------------------------------

# Get the current directory of `run.py`
current_dir = os.path.dirname(os.path.abspath(__file__))

# Navigate up to the project root (parent of "expariment"), then add "src" to the path
project_root = os.path.dirname(current_dir)
sys.path.append(os.path.join(project_root, 'src'))

# Import necessary modules
from config_loader import ConfigLoader
from llm_setup import LLMSetup
from crew_setup import CrewSetup
from models import ProjectPlan
from utils import DisplayUtils

# Initialize components
config_loader = ConfigLoader()
configs = config_loader.load_configs()
llm = LLMSetup.get_llm()

# Setup crew
crew_setup = CrewSetup(configs['agents'], configs['tasks'], llm)
agents = crew_setup.create_agents()
tasks = crew_setup.create_tasks(agents)
crew = crew_setup.assemble_crew(agents, tasks)

# Prepare and display project details
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

DisplayUtils.show_markdown(DisplayUtils.format_project_details(project_data))

# Run the crew
inputs = {
    'project_type': project_data['project'],
    'project_objectives': project_data['project_objectives'],
    'industry': project_data['industry'],
    'team_members': project_data['team_members'],
    'project_requirements': project_data['project_requirements']
}

result = crew.kickoff(inputs=inputs)