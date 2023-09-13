from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, datetime
from webapp import db
from sqlalchemy import event


now = datetime.now()


class AuthValidationError(Exception):
    pass


class User(db.Model):
    """
    Model for authenticating users on the web interface.

    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), nullable=False, unique=True, index=True)
    username = db.Column(db.String(80), unique=True, index=True)
    password = db.Column(db.String(200), nullable=False)
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    active = db.Column(db.Boolean)
    created_on = db.Column(db.DateTime, default=date.today, index=True)
    last_login = db.Column(db.String(80))
    role = db.Column(db.String(20), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, name, surname, email,
                 password, role, active=True):
        # Set email to lower case
        email = email.lower()
        self.fname = name
        self.lname = surname
        self.email = email

        if db.session.query(User).filter_by(email=email).count():
            raise AuthValidationError("Duplicate email found.")
        else:
            self.username = email

        self.password = generate_password_hash(password, method='scrypt')

        role = str.upper(role)
        accepted_roles = {'ADMIN', 'MANAGER'}
        if role in accepted_roles:
            self.role = role
        else:
            raise AuthValidationError("Create User - Role error.")
        self.role = role
        self.active = active

    def get_list():
        """Return a list of all users"""
        return db.session.query(User).all()

    def get(id):
        """Return a user based on id in DB"""
        return db.session.query(User).get(int(id))

    def get_by_mail(email):
        """Return a user based on email in DB"""
        return db.session.query(User).filter_by(email=email.lower()).first()

    def create(self):
        """Create new user."""
        db.session.add(self)
        db.session.commit()
        return self

    def modify(id, name, surname, email, username, role, active):
        """Modify a user."""
        # Set email to lower case
        email = email.lower()

        # Check if this is the last ADMIN user. If yes, dont de-activate.
        admin_user_count = db.session.query(
            User).filter_by(role="ADMIN").count()

        user = db.session.query(User).get(int(id))

        if user.role == 'ADMIN' and admin_user_count <= 1 and active is False:
            raise AuthValidationError("Modify User - Cant disable \
                                        the last ADMIN user.")
        if name != user.fname:
            user.fname = name

        if surname != user.lname:
            user.lname = surname

        if user.email == email:
            user.email = email
        else:
            # check if the new email address already exists in the DB
            check_mail = db.session.query(User).filter_by(email=email).count()
            if check_mail > 0:
                raise AuthValidationError("Modify User - A duplicate email \
                                            address was found.")
            else:
                user.email = email

        if user.username == email:
            user.username = email
        else:
            # Check if the username exists, if not use it, else error
            check_username = db.session.query(
                User).filter_by(username=email).count()
            if check_username > 0:
                raise AuthValidationError("Modify User - A duplicate username \
                                            was found.")
            else:
                user.username = email

        role = str.upper(role)
        accepted_roles = {'ADMIN', 'MANAGER'}
        if role in accepted_roles:
            user.role = role
        else:
            raise AuthValidationError("Modify User - User role incorrect.")

        user.active = active
        db.session.commit()

    def delete(id):
        """Delete a user."""
        # Check if this is the last ADMIN user. If yes, dont delete.
        admin_user_count = db.session.query(
            User).filter_by(role="ADMIN").count()

        user = db.session.query(User).get(int(id))

        if user.role == 'ADMIN' and admin_user_count <= 1:
            raise AuthValidationError("Delete User - Cant delete \
                                        the last ADMIN user.")
        else:
            db.session.query(User).filter_by(id=id).delete()
            db.session.commit()

    def create_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='scrypt')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def set_password(id, password):
        user = db.session.query(User).get(int(id))
        user.password = generate_password_hash(password, method='scrypt')
        db.session.commit()

    def set_user_role(self, user_role):
        role = str.upper(user_role)
        accepted_roles = {'ADMIN', 'MANAGER', 'USER'}
        if role in accepted_roles:
            self.role = role
        else:
            return -1

    def check_user_role(self, user_role):
        """ Returns True if user has role"""
        role = str.upper(user_role)
        accepted_roles = {'ADMIN', 'MANAGER', 'USER'}
        if role in accepted_roles:
            if role == self.role:
                return True
            else:
                return False
        return -1

    def set_last_login(self):
        self.last_login = now.strftime("%m/%d/%Y, %H:%M:%S")
        db.session.commit()
        return self

    def set_user_active(self, state):
        self.active = state

    def check_user_active(self):
        return self.active

    def is_active(self):
        return self.active

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def email_exists(email):
        """Return True if email exists in DB"""
        if db.session.query(User).filter_by(email=email.lower()).first():
            return True
        else:
            return False

    def __repr__(self):
        return f'User: {self.fname} {self.lname}'


# @event.listens_for(User.__table__, 'after_create')
def create_users(*args, **kwargs):
    new_admin = User('Admin', 'Admin',
                     'admin@example.com',
                     'password123', 'admin')
    User.create(new_admin)
    db.session.commit()
