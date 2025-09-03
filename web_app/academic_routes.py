from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from core import academic_calendar_controller
from core import class_management_controller
from core import student_class_assignment_controller
from core import student_controller

academic_bp = Blueprint('academic', __name__, template_folder='templates')

@academic_bp.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
    if request.method == 'POST':
        if 'year' in request.form: # Adding a new year
            year = request.form['year']
            result = academic_calendar_controller.add_academic_year(year)
            if result is True:
                flash('Academic year added successfully!', 'success')
            else:
                flash(f'Error: {result}', 'danger')
        elif 'term_name' in request.form: # Adding a new term
            name = request.form['term_name']
            year_id = request.form['academic_year_id']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            if academic_calendar_controller.add_term(name, year_id, start_date, end_date):
                flash('Term added successfully!', 'success')
            else:
                flash('Error adding term.', 'danger')
        return redirect(url_for('academic.calendar'))

    years = academic_calendar_controller.get_all_academic_years()
    # For simplicity, we'll just show terms for the first year on initial load
    terms_to_display = []
    if years:
        terms_to_display = academic_calendar_controller.get_terms_by_year(years[0][0])

    return render_template('academic_calendar.html', years=years, terms=terms_to_display)

@academic_bp.route('/classes', methods=['GET', 'POST'])
@login_required
def classes():
    if request.method == 'POST':
        if 'class_name' in request.form: # Adding a new class
            class_name = request.form['class_name']
            result = class_management_controller.add_class(class_name)
            if result is True:
                flash('Class added successfully!', 'success')
            else:
                flash(f'Error: {result}', 'danger')
        elif 'section_name' in request.form: # Adding a new section
            section_name = request.form['section_name']
            class_id = request.form['class_id']
            if class_management_controller.add_section(section_name, class_id):
                flash('Section added successfully!', 'success')
            else:
                flash('Error adding section.', 'danger')
        return redirect(url_for('academic.classes'))

    classes = class_management_controller.get_all_classes()
    sections_to_display = []
    if classes:
        sections_to_display = class_management_controller.get_sections_by_class(classes[0][0])
    return render_template('class_management.html', classes=classes, sections=sections_to_display)

@academic_bp.route('/assign_student', methods=['GET', 'POST'])
@login_required
def assign_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        section_id = request.form['section_id']
        term_id = request.form['term_id']
        student_class_assignment_controller.assign_student_to_class(student_id, section_id, term_id)
        return redirect(url_for('academic.assign_student'))

    students = student_controller.get_student_names()
    terms = academic_calendar_controller.get_all_terms()
    sections = class_management_controller.get_all_sections()
    assignments = student_class_assignment_controller.get_class_assignments()
    return render_template('student_class_assignment.html', students=students, terms=terms, sections=sections, assignments=assignments)
