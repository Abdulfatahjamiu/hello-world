import sqlite3
from datetime import datetime
import shutil
import os
from .config import DATABASE_PATH

def add_student(name, dob, address1, city, state, zip_code, class_name, gender, medical_info, photo_path, parent_id):
    """
    Adds a new student to the database.
    """
    try:
        # Handle photo upload
        new_photo_path = ""
        if photo_path:
            # Construct path relative to this file's location to find project root
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            upload_dir = os.path.join(project_root, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)

            _, extension = os.path.splitext(photo_path)
            new_filename = f"{name.replace(' ', '_')}_{datetime.now().timestamp()}{extension}"
            dest_path_abs = os.path.join(upload_dir, new_filename)

            shutil.copy(photo_path, dest_path_abs)
            new_photo_path = os.path.join('uploads', new_filename)

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO students (name, date_of_birth, address_line_1, city, state, zip_code, class, gender, medical_info, photo_path, parent_id, registration_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, dob, address1, city, state, zip_code, class_name, gender, medical_info, new_photo_path, parent_id, registration_date))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding student: {e}")
        return False

def get_all_students():
    """
    Retrieves all students from the database.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        # Corrected query with new address fields
        cursor.execute("""
            SELECT s.id, s.name, s.date_of_birth, s.address_line_1, s.city, s.state, s.zip_code, s.class, s.gender, s.medical_info, p.name, s.registration_date
            FROM students s
            LEFT JOIN parents p ON s.parent_id = p.id
        """)
        students = cursor.fetchall()
        conn.close()
        return students
    except Exception as e:
        print(f"Error getting students: {e}")
        return []

def get_student_names():
    """
    Retrieves all student names from the database.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM students")
        student_names = cursor.fetchall()
        conn.close()
        return student_names
    except Exception as e:
        print(f"Error getting student names: {e}")
        return []

def get_student_by_id(student_id):
    """
    Retrieves a single student's details from the database by their ID.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, date_of_birth, address_line_1, city, state, zip_code, class, gender, medical_info, photo_path, parent_id, registration_date FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        conn.close()
        return student
    except Exception as e:
        print(f"Error getting student by ID: {e}")
        return None
