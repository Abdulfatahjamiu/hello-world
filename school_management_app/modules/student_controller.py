import sqlite3
from datetime import datetime

import shutil
import os

def add_student(name, dob, address1, city, state, zip_code, class_name, gender, medical_info, photo_path, parent_id):
    """
    Adds a new student to the database.
    """
    try:
        # Handle photo upload
        new_photo_path = ""
        if photo_path:
            # Create a unique filename to avoid overwrites
            _, extension = os.path.splitext(photo_path)
            new_filename = f"{name.replace(' ', '_')}_{datetime.now().timestamp()}{extension}"

            # The destination path should be relative to the project root
            dest_path = os.path.join('uploads', new_filename)

            # Copy the file
            shutil.copy(photo_path, os.path.join('..', dest_path))
            new_photo_path = dest_path

        conn = sqlite3.connect('../database/school.db')
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
        conn = sqlite3.connect('../database/school.db')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT s.id, s.name, s.date_of_birth, s.address, s.class, s.gender, s.medical_info, p.name, s.registration_date
            FROM students s
            JOIN parents p ON s.parent_id = p.id
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
        conn = sqlite3.connect('../database/school.db')
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
        conn = sqlite3.connect('../database/school.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone()
        conn.close()
        return student
    except Exception as e:
        print(f"Error getting student by ID: {e}")
        return None
