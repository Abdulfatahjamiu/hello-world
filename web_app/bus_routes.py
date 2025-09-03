from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from core import bus_controller
from core import driver_controller
from core import route_controller
from core import student_bus_controller

bus_bp = Blueprint('bus', __name__, template_folder='templates')

# --- Bus Management ---
@bus_bp.route('/buses', methods=['GET', 'POST'])
@login_required
def list_buses():
    if request.method == 'POST':
        bus_number = request.form['bus_number']
        capacity = request.form['capacity']
        if bus_controller.add_bus(bus_number, capacity):
            flash('Bus added successfully!', 'success')
        else:
            flash('Error adding bus.', 'danger')
        return redirect(url_for('bus.list_buses'))

    buses = bus_controller.get_all_buses()
    return render_template('bus_management.html', buses=buses)

# --- Driver Management ---
@bus_bp.route('/drivers', methods=['GET', 'POST'])
@login_required
def list_drivers():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone_number']
        license_num = request.form['license_number']
        if driver_controller.add_driver(name, phone, license_num):
            flash('Driver added successfully!', 'success')
        else:
            flash('Error adding driver.', 'danger')
        return redirect(url_for('bus.list_drivers'))

    drivers = driver_controller.get_all_drivers()
    return render_template('driver_management.html', drivers=drivers)

# --- Route Management ---
@bus_bp.route('/routes', methods=['GET', 'POST'])
@login_required
def list_routes():
    if request.method == 'POST':
        name = request.form['route_name']
        bus_id = request.form['bus_id']
        driver_id = request.form['driver_id']
        if route_controller.add_route(name, bus_id, driver_id):
            flash('Route added successfully!', 'success')
        else:
            flash('Error adding route.', 'danger')
        return redirect(url_for('bus.list_routes'))

    routes = route_controller.get_all_routes()
    buses = bus_controller.get_all_buses()
    drivers = driver_controller.get_all_drivers()
    return render_template('bus_routes.html', routes=routes, buses=buses, drivers=drivers)

# --- Student Assignment ---
@bus_bp.route('/assignments', methods=['GET', 'POST'])
@login_required
def list_assignments():
    if request.method == 'POST':
        student_id = request.form['student_id']
        route_id = request.form['route_id']
        if student_bus_controller.assign_student_to_route(student_id, route_id):
            flash('Student assigned to route successfully!', 'success')
        else:
            flash('Error assigning student to route.', 'danger')
        return redirect(url_for('bus.list_assignments'))

    assignments = student_bus_controller.get_all_assignments()
    students = student_controller.get_student_names()
    routes = route_controller.get_all_routes()
    return render_template('student_bus_assignment.html', assignments=assignments, students=students, routes=routes)
