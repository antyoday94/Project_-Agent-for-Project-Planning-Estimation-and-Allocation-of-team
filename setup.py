# setup.py
from setuptools import setup, find_packages

setup(
    name="agent_project",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'crewai',
        'python-dotenv',
        'pyyaml',
        'ipython',
        'pydantic'
    ],
)