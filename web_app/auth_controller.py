from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from flask import g
from .user import User
from .app import get_db

def get_user_by_username(username):
    db = get_db()
    cursor = db.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    if user_data:
        return User(id=user_data['id'], username=user_data['username'], password_hash=user_data['password_hash'])
    return None

def get_user_by_id(user_id):
    db = get_db()
    cursor = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        return User(id=user_data['id'], username=user_data['username'], password_hash=user_data['password_hash'])
    return None

def create_user(username, password):
    password_hash = User.set_password(password)
    db = get_db()
    try:
        cursor = db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        db.commit()
        return get_user_by_id(cursor.lastrowid)
    except sqlite3.IntegrityError:
        return None # Username already exists
