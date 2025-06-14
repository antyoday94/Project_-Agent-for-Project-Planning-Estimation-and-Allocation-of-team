# File: config_loader.py
import os
import yaml

class ConfigLoader:
    def __init__(self):
        self.base_dir = self._get_base_directory()

    def _get_base_directory(self):
        """Determine the base directory path dynamically"""
        try:
            # Path to this file: /app/backend/src/config_loader.py
            # script_dir: /app/backend/src
            # os.path.dirname(script_dir): /app/backend
            # We need /app, so two levels up from script_dir
            script_dir = os.path.dirname(os.path.abspath(__file__))
            return os.path.dirname(os.path.dirname(script_dir))  # Go up two levels from current file
        except NameError:
            # This NameError case might be for environments like Jupyter notebooks
            # where __file__ is not defined.
            # If current_dir is /app/experiment (assuming notebook is there),
            # os.path.dirname(current_dir) is /app. This seems correct.
            # If current_dir is /app (e.g. running a script from root),
            # os.path.dirname(current_dir) would be /
            # This part needs to be robust. A common pattern is to find a known marker.
            # For now, let's assume the NameError case is less critical for the FastAPI app.
            # The primary path (try block) is what matters for the app.
            current_dir = os.getcwd()
            # If running from /app (e.g. python -m backend.app_FastAPI), cwd is /app
            # This part of the logic might need more robust handling if used outside the FastAPI context
            # For the FastAPI app, __file__ should be defined.
            # Let's adjust it assuming the script is run from a context where __file__ is reliable.
            # If __file__ is not defined, and CWD is /app, then os.path.dirname(current_dir) would be /.
            # A safer approach for the except block, if it's ever hit in a deployed scenario,
            # might be to assume the CWD is the project root or use an environment variable.
            # Given the context, the primary concern is the try block.
            # Modifying the except block to return current_dir if it's the project root.
            # This is heuristic. For now, focus on the 'try' path.
            if os.path.basename(current_dir) == 'experiment': # e.g. /app/experiment
                 return os.path.dirname(current_dir) # /app
            return current_dir # Assume CWD is project root if __file__ not defined

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
