import sqlite3
import os

def create_database():
    """
    Creates the database and tables from schema.txt.
    Assumes this script is in the 'database' directory.
    """
    try:
        # Get the directory of the current script
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Read the schema from the schema.txt file in the same directory
        with open(os.path.join(dir_path, 'schema.txt'), 'r') as f:
            schema = f.read()

        # Create a connection to the database file in the same directory
        conn = sqlite3.connect(os.path.join(dir_path, 'school.db'))
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
