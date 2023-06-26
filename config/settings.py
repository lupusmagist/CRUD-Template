""" Settings File """
from environs import Env

env = Env()
env.read_env()


class Config:
    """ Global config class for app
    Use python-dotenv to import private settings from .env file
    """

    APP_NAME = env.str('APP_NAME')
    SECRET_KEY = env.str('SECRET_KEY')
    CHECK_IN_FAIL_TIME = 1
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # Two MB max upload
    UPLOAD_EXTENSIONS = ['jpg', 'png', 'gif', 'pdf']
    UPLOAD_PATH = 'uploads'
    CRYPT_KEY = env.str('CRYPT_KEY')


class ProductionConfig(Config):
    if env.str('USE_POSTGRES') == 0:
        POSTGRES_USER = env.str('POSTGRES_USER')
        POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD')
        POSTGRES_DB = env.str('POSTGRES_DB')
        POSTGRES_SERVER = env.str('POSTGRES_SERVER')
        SQLALCHEMY_DATABASE_URI = 'postgresql://' \
            + POSTGRES_USER \
            + ':' \
            + POSTGRES_PASSWORD \
            + '@' \
            + POSTGRES_SERVER \
            + '/' \
            + POSTGRES_DB
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite'

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    if env.str('USE_POSTGRES') == 0:
        POSTGRES_USER = env.str('POSTGRES_USER')
        POSTGRES_PASSWORD = env.str('POSTGRES_PASSWORD')
        POSTGRES_DB = env.str('POSTGRES_DB')
        POSTGRES_SERVER = env.str('POSTGRES_SERVER')
        SQLALCHEMY_DATABASE_URI = 'postgresql://' \
            + POSTGRES_USER \
            + ':' \
            + POSTGRES_PASSWORD \
            + '@' \
            + POSTGRES_SERVER \
            + '/' \
            + POSTGRES_DB
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'mail.danchan.co.za'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = env.str('EMAIL_USER')
    MAIL_PASSWORD = env.str('EMAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'danie@danchan.co.za'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
