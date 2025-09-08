from .config import DATABASE_PATH
import sqlite3

def add_class(name):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO classes (name) VALUES (?)", (name,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return "Class already exists"
    except Exception as e:
        print(f"Error adding class: {e}")
        return False

def get_all_classes():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM classes")
        classes = cursor.fetchall()
        conn.close()
        return classes
    except Exception as e:
        print(f"Error getting classes: {e}")
        return []

def add_section(name, class_id):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sections (name, class_id) VALUES (?, ?)", (name, class_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding section: {e}")
        return False

def get_sections_by_class(class_id):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sections WHERE class_id = ?", (class_id,))
        sections = cursor.fetchall()
        conn.close()
        return sections
    except Exception as e:
        print(f"Error getting sections: {e}")
        return []

def get_all_sections():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.name, c.name
            FROM sections s
            JOIN classes c ON s.class_id = c.id
        """)
        sections = cursor.fetchall()
        conn.close()
        return sections
    except Exception as e:
        print(f"Error getting all sections: {e}")
        return []
