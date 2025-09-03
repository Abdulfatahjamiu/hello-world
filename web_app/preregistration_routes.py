from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from core import preregistration_controller

prereg_bp = Blueprint('prereg', __name__, template_folder='templates')

@prereg_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    if request.method == 'POST':
        name = request.form['parentName']
        email = request.form['email']
        phone = request.form['phoneNumber']
        # The form in the template is simpler than the desktop app's
        # I will add the missing fields later if needed.
        # For now, I'll pass empty strings for the other fields.
        child_name = ""
        child_age = 0
        notes = ""
        follow_up_date = ""
        next_of_kin_name = ""
        next_of_kin_phone = ""

        if preregistration_controller.add_parent(name, phone, email, child_name, child_age, notes, follow_up_date, next_of_kin_name, next_of_kin_phone):
            flash('New parent inquiry has been successfully submitted!', 'success')
            return redirect(url_for('prereg.list_inquiries'))
        else:
            flash('Error submitting inquiry. Please try again.', 'danger')

    return render_template('preregistration.html')

@prereg_bp.route('/')
@login_required
def list_inquiries():
    parents = preregistration_controller.get_all_parents()
    # I need a new template to display this list. I will create `preregistration_list.html`
    return render_template('preregistration_list.html', parents=parents)
