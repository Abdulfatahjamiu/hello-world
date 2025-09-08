from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from core import payment_controller
from core import student_controller

pay_bp = Blueprint('pay', __name__, template_folder='templates')

@pay_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        amount = request.form.get('amount')
        account = request.form.get('account')
        payment_date = request.form.get('payment_date')
        academic_year = request.form.get('academic_year')
        term = request.form.get('term')

        if payment_controller.add_payment(student_id, amount, account, payment_date, academic_year, term):
            flash('Payment recorded successfully!', 'success')
            return redirect(url_for('pay.history'))
        else:
            flash('Error recording payment.', 'danger')

    # For the form, we need a list of students
    students = student_controller.get_student_names()
    return render_template('payment_fees.html', students=students) # Using payment_fees for now

@pay_bp.route('/')
@login_required
def history():
    payments = payment_controller.get_all_payments()
    return render_template('payment_history.html', payments=payments)
