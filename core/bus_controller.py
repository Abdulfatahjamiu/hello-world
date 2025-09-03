from .config import DATABASE_PATH
import sqlite3

def add_bus(bus_number, capacity):
    """
    Adds a new bus to the database.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO buses (bus_number, capacity) VALUES (?, ?)", (bus_number, capacity))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding bus: {e}")
        return False

def get_all_buses():
    """
    Retrieves all buses from the database.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM buses")
        buses = cursor.fetchall()
        conn.close()
        return buses
    except Exception as e:
        print(f"Error getting buses: {e}")
        return []
