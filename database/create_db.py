import sqlite3

def create_database():
    """
    Creates the database and tables for the school management app.
    """
    try:
        # Read the schema from the schema.txt file
        with open('schema.txt', 'r') as f:
            schema = f.read()

        # Create a connection to the database
        conn = sqlite3.connect('school.db')
        cursor = conn.cursor()

        # Execute the schema to create the tables
        cursor.executescript(schema)

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        print("Database 'school.db' created successfully.")

    except Exception as e:
        print(f"Error creating database: {e}")

if __name__ == '__main__':
    create_database()
