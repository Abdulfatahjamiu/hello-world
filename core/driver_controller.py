from .config import DATABASE_PATH
import sqlite3

def add_driver(name, phone_number, license_number):
    """
    Adds a new driver to the database.
    """
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO drivers (name, phone_number, license_number) VALUES (?, ?, ?)",
                (name, phone_number, license_number)
            )
            conn.commit()
            return True
    except Exception as e:
        print(f"Error adding driver: {e}")
        return False

def get_all_drivers():
    """
    Retrieves all drivers from the database.
    """
    try:
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM drivers")
            drivers = cursor.fetchall()
            return drivers
    except Exception as e:
        print(f"Error getting drivers: {e}")
        return []
