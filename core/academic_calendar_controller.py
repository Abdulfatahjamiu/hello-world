from .config import DATABASE_PATH
import sqlite3

def add_academic_year(year):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO academic_years (year) VALUES (?)", (year,))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return "Year already exists"
    except Exception as e:
        print(f"Error adding academic year: {e}")
        return False

def get_all_academic_years():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM academic_years")
        years = cursor.fetchall()
        conn.close()
        return years
    except Exception as e:
        print(f"Error getting academic years: {e}")
        return []

def add_term(name, year_id, start_date, end_date):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO terms (name, academic_year_id, start_date, end_date) VALUES (?, ?, ?, ?)", (name, year_id, start_date, end_date))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding term: {e}")
        return False

def get_terms_by_year(year_id):
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM terms WHERE academic_year_id = ?", (year_id,))
        terms = cursor.fetchall()
        conn.close()
        return terms
    except Exception as e:
        print(f"Error getting terms: {e}")
        return []

def get_all_terms():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, t.name, ay.year
            FROM terms t
            JOIN academic_years ay ON t.academic_year_id = ay.id
        """)
        terms = cursor.fetchall()
        conn.close()
        return terms
    except Exception as e:
        print(f"Error getting all terms: {e}")
        return []
