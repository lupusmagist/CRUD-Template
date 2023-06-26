from flask import Blueprint, render_template, redirect, url_for, request, flash
from webapp import db
from webapp.models.user_auth import User
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='templates',
                 static_folder='static', static_url_path='/auth/static')


@auth.route('/', methods=['GET'])
def home():
    return render_template('auth/login.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        # Check if the username is a email address
        if '@' in username:
            # Might be email, checking as such

            # if this returns a user, then the email already exists in database
            user = db.session.query(User).filter_by(email=username).first()

            # check if user actually exists
            # take the user supplied password, hash it, and compare it to
            # the hashed password in database
            if not user:
                flash('Please check your login details and try again.')
                # if user doesn't exist or password is wrong, reload the page
                return redirect(url_for('auth.login'))

            if not user.check_password(password):
                flash('Please check your login details and try again.')
                # if user doesn't exist or password is wrong, reload the page
                return redirect(url_for('auth.login'))

            if not user.check_user_active():
                flash('Your account is disabled.' +
                      'Please contact system support')
                # if user doesn't exist or password is wrong, reload the page
                return redirect(url_for('auth.login'))

            # if the above check passes, then we know the user has the
            # right credentials
            login_user(user, remember=remember)
            # Saving last login time
            user.set_last_login()
            return redirect(url_for('main.index'))

        else:
            # Might be a username
            # if this returns a user, then the email already exists in database
            user = db.session.query(User).filter_by(username=username).first()

            # check if user actually exists
            # take the user supplied password, hash it, and compare it to
            # the hashed password in database
            if not user:
                flash('Please check your login details and try again.')
                # if user doesn't exist or password is wrong, reload the page
                return redirect(url_for('auth.login'))

            if not user.check_password(password):
                flash('Please check your login details and try again.')
                # if user doesn't exist or password is wrong, reload the page
                return redirect(url_for('auth.login'))

            if not user.check_user_active():
                flash('Your account is disabled.' +
                      'Please contact system support')
                # if user doesn't exist or password is wrong, reload the page
                return redirect(url_for('auth.login'))

            # if the above check passes, then we know the user has the
            # right credentials
            login_user(user, remember=remember)
            # Saving last login time
            user.set_last_login()
            return redirect(url_for('main.index'))


@ auth.route('/logout')
@ login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@ auth.route('/change_password/<int:id>')
@ login_required
def change_password(id):

    user = db.session.query(User).get(int(id))

    return render_template('auth/password.html', user=user)


@ auth.route('/password', methods=['POST'])
@ login_required
def password():
    id = request.form.get('id')
    password = request.form.get('password')

    user = db.session.query(User).filter_by(id=id).first()
    user.set_password(password)

    db.session.commit()

    return redirect(url_for('auth.manage_user'))
