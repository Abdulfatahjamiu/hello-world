import sqlite3
from .config import DATABASE_PATH

def add_driver(name, phone_number, license_number):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO drivers (name, phone_number, license_number) VALUES (?, ?, ?)", (name, phone_number, license_number))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding driver: {e}")
        return False

def get_all_drivers():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM drivers")
        drivers = cursor.fetchall()
        conn.close()
        return drivers
    except Exception as e:
        print(f"Error getting drivers: {e}")
        return []
