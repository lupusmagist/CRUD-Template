from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from webapp import role_required
from webapp.models.user_auth import User, AuthValidationError
import re

aum = Blueprint('aum', __name__, template_folder='templates',
                static_folder='static',
                static_url_path='/aum/static')


@aum.before_request
@role_required('ADMIN')
def before_request():
    """ Protect all of the admin endpoints. """
    pass


@aum.route('/', methods=['GET'])
def index():
    return render_template('aum/index.html', user_list=User.get_list())


@aum.route('/user_add', methods=['GET', 'POST'])
def user_add():
    if request.method == 'GET':
        return render_template('aum/user.html', new_user=True)
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        if request.form.get('active'):
            active = True
        else:
            active = False

        # if this returns a user, then the email already exists in database
        # if a user is found, we want to redirect back to start page
        if User.get_by_mail(email):
            flash('Email address already exists', 'alert-danger')
            return redirect(url_for('aum.user_add'))

        # create new user with the form data. Hash the password so plaintext
        # version isn't saved.
        new_user = User(fname, lname, email, password, role, active)
        User.create(new_user)

        flash(f'User Created Successfully', 'alert-success')
        return redirect(url_for('aum.index'))


@aum.route('/user_modify/<int:id>', methods=['GET', 'POST'])
def user_modify(id):
    if request.method == 'GET':
        return render_template('aum/user.html', new_user=False, user=User.get(id))

    if request.method == 'POST':
        if request.form.get('active'):
            active = True
        else:
            active = False

        try:
            User.modify(id,
                        request.form.get('fname'),
                        request.form.get('lname'),
                        request.form.get('email'),
                        request.form.get('email'),
                        request.form.get('role'),
                        active)

            flash(f'User Updated Successfully', 'alert-success')
            return redirect(url_for('aum.index'))

        except AuthValidationError as exception:
            flash(f'{exception}', 'alert-danger')
            return render_template('aum/user.html', new_user=False, user=User.get(id))


@aum.route('/user_delete/<int:id>')
def user_delete(id):
    try:
        User.delete(id)
        flash(f'User Deleted Successfully', 'alert-success')
        return redirect(url_for('aum.index'))
    except AuthValidationError as exception:
        flash(f'Failed to delete user', 'alert-danger')
        return redirect(url_for('aum.index'))


@aum.route('/user_validate_mail/<email>')
def user_validate_mail(email):
    # Checks if the email address is valid
    # Checks if the email address exists in DB
    mail_address_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if (re.fullmatch(mail_address_regex, email)):
        if User.email_exists(email):
            message = {'status': 'NOK', 'message': 'Existing email found'}
        else:
            message = {'status': 'OK', 'message': ''}
    else:
        message = {'status': 'NOK', 'message': 'Invalid email address'}

    return jsonify(message)


@aum.route('/change_password/<int:id>', methods=['POST'])
def change_password(id):
    print(request.form.get('password'))
    if request.method == 'POST':
        try:
            User.set_password(id, request.form.get('password'))
            flash(f'Password changed successfully', 'alert-success')
            return render_template('aum/user.html', new_user=False, user=User.get(id))
        except AuthValidationError as exception:
            flash(f'Password change failed', 'alert-danger')
            return render_template('aum/user.html', new_user=False, user=User.get(id))
