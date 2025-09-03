import sqlite3
from .config import DATABASE_PATH

def add_payment(student_id, amount, account, payment_date, academic_year, term):
    """
    Adds a new payment to the database.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO payments (student_id, amount, account, payment_date, academic_year, term)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, amount, account, payment_date, academic_year, term))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error adding payment: {e}")
        return False

def get_all_payments():
    """
    Retrieves all payments from the database.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, s.name, p.amount, p.account, p.payment_date, p.academic_year, p.term
            FROM payments p
            JOIN students s ON p.student_id = s.id
        """)
        payments = cursor.fetchall()
        conn.close()
        return payments
    except Exception as e:
        print(f"Error getting payments: {e}")
        return []

def get_payments_by_filter(student_id=None, start_date=None, end_date=None, account=None, academic_year=None, term=None):
    """
    Retrieves payments from the database based on filters.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        query = """
            SELECT p.id, s.name, p.amount, p.account, p.payment_date, p.academic_year, p.term
            FROM payments p
            JOIN students s ON p.student_id = s.id
            WHERE 1=1
        """
        params = []
        if student_id:
            query += " AND s.id = ?"
            params.append(student_id)
        if start_date:
            query += " AND p.payment_date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND p.payment_date <= ?"
            params.append(end_date)
        if account:
            query += " AND p.account = ?"
            params.append(account)
        if academic_year:
            query += " AND p.academic_year = ?"
            params.append(academic_year)
        if term:
            query += " AND p.term = ?"
            params.append(term)
        cursor.execute(query, params)
        payments = cursor.fetchall()
        conn.close()
        return payments
    except Exception as e:
        print(f"Error getting filtered payments: {e}")
        return []
