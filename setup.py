from setuptools import find_packages
from setuptools import setup
from environs import Env

env = Env()
env.read_env()

setup(
    name=env.str('APP_NAME'),
    version="0.0.1",
    url="github url",
    license="",
    maintainer="D. Cornelius",
    maintainer_email="lupusmagist@gmail.com",
    description=env.str('APP_DESCRIPTION'),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask>=2.0', 'flask-sqlalchemy>=2.4',
        'flask_login>=0.5', 'flask-migrate>=2.5', 'gunicorn>=20',
        'psycopg2-binary>=2.8',],
    python_requires='>=3.10',
    extras_require={"test": ["pytest", "coverage"]},
)
