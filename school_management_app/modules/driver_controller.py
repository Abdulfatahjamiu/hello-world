import sqlite3

def add_driver(name, phone_number, license_number):
    """
    Adds a new driver to the database.
    """
    try:
        conn = sqlite3.connect('../database/school.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO drivers (name, phone_number, license_number) VALUES (?, ?, ?)", (name, phone_number, license_number))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding driver: {e}")
        return False

def get_all_drivers():
    """
    Retrieves all drivers from the database.
    """
    try:
        conn = sqlite3.connect('../database/school.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM drivers")
        drivers = cursor.fetchall()
        conn.close()
        return drivers
    except Exception as e:
        print(f"Error getting drivers: {e}")
        return []
