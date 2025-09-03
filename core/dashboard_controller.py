import sqlite3
from .config import DATABASE_PATH

def get_dashboard_stats():
    """
    Retrieves statistics for the dashboard.
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(amount) FROM payments")
        total_payments = cursor.fetchone()[0] or 0

        cursor.execute("SELECT COUNT(*) FROM parents WHERE follow_up_date IS NOT NULL")
        pending_preregistrations = cursor.fetchone()[0]

        cursor.execute("SELECT account, SUM(amount) FROM payments GROUP BY account")
        payment_breakdown = cursor.fetchall()

        conn.close()

        return {
            "total_students": total_students,
            "total_payments": total_payments,
            "pending_preregistrations": pending_preregistrations,
            "payment_breakdown": payment_breakdown
        }
    except Exception as e:
        print(f"Error getting dashboard stats: {e}")
        return {
            "total_students": 0,
            "total_payments": 0,
            "pending_preregistrations": 0,
            "payment_breakdown": []
        }
