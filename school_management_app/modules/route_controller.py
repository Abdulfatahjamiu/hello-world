import sqlite3

def add_route(name, bus_id, driver_id):
    """
    Adds a new route to the database.
    """
    try:
        conn = sqlite3.connect('../database/school.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO routes (name, bus_id, driver_id) VALUES (?, ?, ?)", (name, bus_id, driver_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding route: {e}")
        return False

def get_all_routes():
    """
    Retrieves all routes from the database.
    """
    try:
        conn = sqlite3.connect('../database/school.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, r.name, b.bus_number, d.name
            FROM routes r
            JOIN buses b ON r.bus_id = b.id
            JOIN drivers d ON r.driver_id = d.id
        """)
        routes = cursor.fetchall()
        conn.close()
        return routes
    except Exception as e:
        print(f"Error getting routes: {e}")
        return []

def get_bus_numbers():
    """
    Retrieves all bus numbers from the database.
    """
    try:
        conn = sqlite3.connect('../database/school.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, bus_number FROM buses")
        buses = cursor.fetchall()
        conn.close()
        return buses
    except Exception as e:
        print(f"Error getting bus numbers: {e}")
        return []

def get_driver_names():
    """
    Retrieves all driver names from the database.
    """
    try:
        conn = sqlite3.connect('../database/school.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM drivers")
        drivers = cursor.fetchall()
        conn.close()
        return drivers
    except Exception as e:
        print(f"Error getting driver names: {e}")
        return []
