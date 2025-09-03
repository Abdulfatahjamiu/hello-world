import sqlite3
from .config import DATABASE_PATH

def add_route(name, bus_id, driver_id):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO routes (name, bus_id, driver_id) VALUES (?, ?, ?)", (name, bus_id, driver_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding route: {e}")
        return False

def get_all_routes():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, r.name, b.bus_number, d.name
            FROM routes r
            LEFT JOIN buses b ON r.bus_id = b.id
            LEFT JOIN drivers d ON r.driver_id = d.id
        """)
        routes = cursor.fetchall()
        conn.close()
        return routes
    except Exception as e:
        print(f"Error getting routes: {e}")
        return []

def get_route_names():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM routes")
        routes = cursor.fetchall()
        conn.close()
        return routes
    except Exception as e:
        print(f"Error getting route names: {e}")
        return []
