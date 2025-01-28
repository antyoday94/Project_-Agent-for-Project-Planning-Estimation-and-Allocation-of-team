# File: crew_setup.py
from crewai import Agent, Task, Crew
from models import ProjectPlan

class CrewSetup:
    def __init__(self, agents_config, tasks_config, llm):
        self.agents_config = agents_config
        self.tasks_config = tasks_config
        self.llm = llm
        
    def create_agents(self):
        """Instantiate all agents"""
        return {
            'project_planning_agent': Agent(
                config=self.agents_config['project_planning_agent'],
                llm=self.llm
            ),
            'estimation_agent': Agent(
                config=self.agents_config['estimation_agent'],
                llm=self.llm
            ),
            'resource_allocation_agent': Agent(
                config=self.agents_config['resource_allocation_agent'],
                llm=self.llm
            )
        }
    
    def create_tasks(self, agents):
        """Create all tasks"""
        return {
            'task_breakdown': Task(
                config=self.tasks_config['task_breakdown'],
                agent=agents['project_planning_agent']
            ),
            'time_resource_estimation': Task(
                config=self.tasks_config['time_resource_estimation'],
                agent=agents['estimation_agent']
            ),
            'resource_allocation': Task(
                config=self.tasks_config['resource_allocation'],
                agent=agents['resource_allocation_agent'],
                output_pydantic=ProjectPlan
            )
        }
    
    def assemble_crew(self, agents, tasks):
        """Assemble the complete crew"""
        return Crew(
            agents=list(agents.values()),
            tasks=list(tasks.values()),
            verbose=True
        )