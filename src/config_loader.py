# File: config_loader.py
import os
import yaml

class ConfigLoader:
    def __init__(self):
        self.base_dir = self._get_base_directory()
        
    def _get_base_directory(self):
        """Determine the base directory path dynamically"""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            return os.path.dirname(script_dir)  # Go up one level from current file
        except NameError:
            current_dir = os.getcwd()
            return os.path.dirname(current_dir)  # Go up from notebook directory
            
    def load_configs(self):
        """Load all YAML configurations"""
        config_paths = {
            'agents': os.path.join(self.base_dir, 'config', 'agents.yaml'),
            'tasks': os.path.join(self.base_dir, 'config', 'tasks.yaml')
        }
        
        configs = {}
        for config_type, path in config_paths.items():
            with open(path, 'r') as file:
                configs[config_type] = yaml.safe_load(file)
        return configs