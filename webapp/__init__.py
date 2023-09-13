from functools import wraps
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.
    We pass in the config that we want to use in the settings file

    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    # app.config.from_object('config.settings')
    # app.config.from_pyfile('settings.py', silent=True)

    if app.config['DEBUG']:
        app.config.from_object('config.settings.DevelopmentConfig')
        print('Running in debug mode')
    else:
        app.config.from_object('config.settings.ProductionConfig')
        print('Running in production mode')

    db.init_app(app)

    from webapp.models.user_auth import User, create_users

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_mail(user_id)

    from webapp.blueprints.main import main
    from webapp.blueprints.auth import auth
    from webapp.blueprints.aum import aum
    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(aum, url_prefix='/aum')

    @app.cli.command("create-database")
    def create_database():
        print(app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all()

    @app.cli.command("drop-database")
    def drop_database():
        db.drop_all()

    @app.cli.command("create-default-users")
    def create_user():
        create_users()

    return app


def role_required(role: str):
    def _role_required(f):
        @ wraps(f)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if not current_user.check_user_role(role):
                return 'Forbidden', 403
            return f(*args, **kwargs)
        return decorated_view
    return _role_required


def roles_required(roles: list, require_all=False):
    def _roles_required(f):
        @ wraps(f)
        def decorated_view(*args, **kwargs):
            if len(roles) == 0:
                raise ValueError('Empty list used when requiring a role.')
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if require_all and not all(
                    current_user.check_user_role(role) for role in roles):
                return 'Forbidden', 403
            elif not require_all and not any(
                    current_user.check_user_role(role) for role in roles):
                return 'Forbidden', 403
            return f(*args, **kwargs)
        return decorated_view
    return _roles_required
