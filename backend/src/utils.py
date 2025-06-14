# File: utils.py
from IPython.display import display, Markdown

class DisplayUtils:
    @staticmethod
    def format_project_details(project_data):
        """Format project details for display"""
        return f"""
        **Project Type:** {project_data['project']}
        **Project Objectives:** {project_data['project_objectives']}
        **Industry:** {project_data['industry']}
        **Team Members:**{project_data['team_members']}
        **Project Requirements:**{project_data['project_requirements']}
        """
    
    @staticmethod
    def show_markdown(content):
        """Display Markdown content in notebook"""
        display(Markdown(content))
