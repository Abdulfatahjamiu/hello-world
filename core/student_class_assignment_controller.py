import sqlite3
from .config import DATABASE_PATH

def assign_student_to_class(student_id, section_id, term_id):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student_class_assignments WHERE student_id = ? AND term_id = ?", (student_id, term_id))
        if cursor.fetchone():
            return "Student already assigned for this term"
        cursor.execute("INSERT INTO student_class_assignments (student_id, section_id, term_id) VALUES (?, ?, ?)", (student_id, section_id, term_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error assigning student to class: {e}")
        return False

def get_class_assignments():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.name, c.name, sec.name, t.name, ay.year
            FROM student_class_assignments sca
            JOIN students s ON sca.student_id = s.id
            JOIN sections sec ON sca.section_id = sec.id
            JOIN classes c ON sec.class_id = c.id
            JOIN terms t ON sca.term_id = t.id
            JOIN academic_years ay ON t.academic_year_id = ay.id
        """)
        assignments = cursor.fetchall()
        conn.close()
        return assignments
    except Exception as e:
        print(f"Error getting class assignments: {e}")
        return []
