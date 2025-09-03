from werkzeug.security import generate_password_hash
from .user import User
import sqlite3

def get_user_by_username(db, username):
    cursor = db.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    if user_data:
        return User(id=user_data['id'], username=user_data['username'], password_hash=user_data['password_hash'])
    return None

def get_user_by_id(db, user_id):
    cursor = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        return User(id=user_data['id'], username=user_data['username'], password_hash=user_data['password_hash'])
    return None

def create_user(db, username, password):
    password_hash = User.set_password(password)
    try:
        cursor = db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        db.commit()
        new_user_id = cursor.lastrowid
        return get_user_by_id(db, new_user_id)
    except sqlite3.IntegrityError:
        db.rollback()
        return None
