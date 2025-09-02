import sqlite3
from datetime import datetime

def add_parent(name, phone_number, email, child_name, child_age, notes, follow_up_date, next_of_kin_name, next_of_kin_phone):
    """
    Adds a new parent to the database.
    """
    try:
        conn = sqlite3.connect('../database/school.db')
        cursor = conn.cursor()

        enquiry_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO parents (name, phone_number, email, child_name, child_age, enquiry_date, notes, follow_up_date, next_of_kin_name, next_of_kin_phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, phone_number, email, child_name, child_age, enquiry_date, notes, follow_up_date, next_of_kin_name, next_of_kin_phone))

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding parent: {e}")
        return False

def get_all_parents():
    """
    Retrieves all parents from the database.
    """
    try:
        conn = sqlite3.connect('../database/school.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM parents")
        parents = cursor.fetchall()

        conn.close()
        return parents
    except Exception as e:
        print(f"Error getting parents: {e}")
        return []

def get_parent_names():
    """
    Retrieves all parent names from the database.
    """
    try:
        conn = sqlite3.connect('../database/school.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, name FROM parents")
        parent_names = cursor.fetchall()

        conn.close()
        return parent_names
    except Exception as e:
        print(f"Error getting parent names: {e}")
        return []
