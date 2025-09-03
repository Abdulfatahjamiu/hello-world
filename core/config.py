import os

# Define the absolute path to the project root directory
# This assumes the 'core' directory is at the root of the project.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define the database path relative to the project root
DATABASE_NAME = 'school.db'
DATABASE_PATH = os.path.join(PROJECT_ROOT, 'database', DATABASE_NAME)
