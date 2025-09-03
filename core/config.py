import os
import sys

def get_project_root():
    """
    Finds the project root dynamically.
    This allows the app to be run from different locations.
    """
    # If running as a PyInstaller bundle
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    # If running as a script
    # Assumes 'core' is a direct child of the project root
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PROJECT_ROOT = get_project_root()
DATABASE_NAME = 'school.db'
DATABASE_PATH = os.path.join(PROJECT_ROOT, 'database', DATABASE_NAME)
UPLOADS_DIR = os.path.join(PROJECT_ROOT, 'uploads')
