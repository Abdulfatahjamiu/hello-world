from flask import Flask, g, render_template, redirect, url_for
from flask_login import LoginManager, current_user
import sqlite3
import os

# Import blueprints and controllers
from .auth_routes import auth_bp
from .preregistration_routes import prereg_bp
from .enrollment_routes import enroll_bp
from .payment_routes import pay_bp
from .bus_routes import bus_bp
from .academic_routes import academic_bp
from core import auth_controller
from core import dashboard_controller
from core import student_controller
from core import payment_controller
from core import bus_controller
from core import driver_controller
from core import route_controller
from core import student_bus_controller
from core import academic_calendar_controller
from core import class_management_controller
from core import student_class_assignment_controller

# --- App Initialization ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-key-that-should-be-changed'
app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), '..', 'database', 'school.db')

# --- Flask-Login Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    # Use a function that gets a db connection from the app context
    db = get_db()
    return auth_controller.get_user_by_id(db, int(user_id))

# --- Database Connection ---
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# --- Blueprints ---
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(prereg_bp, url_prefix='/preregistration')
app.register_blueprint(enroll_bp, url_prefix='/enrollment')
app.register_blueprint(pay_bp, url_prefix='/payments')
app.register_blueprint(bus_bp, url_prefix='/bus')
app.register_blueprint(academic_bp, url_prefix='/academic')

# A main blueprint for the rest of the app
main_bp = Blueprint('main', __name__, template_folder='templates')

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    stats = dashboard_controller.get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)

app.register_blueprint(main_bp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
