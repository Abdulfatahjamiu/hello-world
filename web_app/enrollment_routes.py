from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from core import student_controller, preregistration_controller # Need parent data

enroll_bp = Blueprint('enroll', __name__, template_folder='templates')

@enroll_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        # Simplified to a single-step process for now
        name = request.form['first-name'] + ' ' + request.form['last-name']
        dob = request.form['dob']
        address1 = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip']
        class_name = "To be assigned" # Placeholder
        gender = request.form['gender']
        # These fields are not in the simple form, so pass empty strings
        medical_info = ""
        photo_path = ""
        parent_id = 1 # Placeholder, should be selected from a dropdown

        if student_controller.add_student(name, dob, address1, city, state, zip_code, class_name, gender, medical_info, photo_path, parent_id):
            flash('Student enrolled successfully!', 'success')
            return redirect(url_for('enroll.list_students'))
        else:
            flash('Error enrolling student.', 'danger')

    return render_template('enrollment_step1.html')

@enroll_bp.route('/list')
@login_required
def list_students():
    students = student_controller.get_all_students()
    return render_template('student_list.html', students=students)
