import sqlite3
from .config import DATABASE_PATH

def assign_student_to_route(student_id, route_id):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO student_bus (student_id, route_id) VALUES (?, ?)", (student_id, route_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error assigning student to route: {e}")
        return False

def get_all_assignments():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, r.id, s.name, r.name, b.bus_number, d.name, sb.pickup_status, sb.dropoff_status
            FROM student_bus sb
            JOIN students s ON sb.student_id = s.id
            JOIN routes r ON sb.route_id = r.id
            LEFT JOIN buses b ON r.bus_id = b.id
            LEFT JOIN drivers d ON r.driver_id = d.id
        """)
        assignments = cursor.fetchall()
        conn.close()
        return assignments
    except Exception as e:
        print(f"Error getting assignments: {e}")
        return []

def update_pickup_status(student_id, route_id, status):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE student_bus SET pickup_status = ? WHERE student_id = ? AND route_id = ?", (status, student_id, route_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating pickup status: {e}")
        return False

def update_dropoff_status(student_id, route_id, status):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE student_bus SET dropoff_status = ? WHERE student_id = ? AND route_id = ?", (status, student_id, route_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error updating dropoff status: {e}")
        return False
