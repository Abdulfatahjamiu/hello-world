import sqlite3
import os

def create_database():
    """
    Creates the database and tables from schema.txt.
    This script is designed to be run from any location and will correctly
    place the database file within the 'database' directory.
    """
    try:
        # Get the directory of the current script
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Read the schema from the schema.txt file in the same directory
        schema_path = os.path.join(dir_path, 'schema.txt')
        with open(schema_path, 'r') as f:
            schema = f.read()

        # Create a connection to the database file in the same directory
        db_path = os.path.join(dir_path, 'school.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Execute the schema to create the tables
        cursor.executescript(schema)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        print("Database 'school.db' created successfully in the 'database' directory.")

    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == '__main__':
    create_database()
