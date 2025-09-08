from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from flask_login import login_user, logout_user, login_required, current_user
from core import auth_controller

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = g.db # Get DB from app context
        user = auth_controller.get_user_by_username(db, username)
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=True)
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = g.db # Get DB from app context
        user = auth_controller.create_user(db, username, password)
        if user is None:
            flash('Username already exists.')
            return redirect(url_for('auth.register'))
        login_user(user)
        return redirect(url_for('main.dashboard'))
    return render_template('register.html')
