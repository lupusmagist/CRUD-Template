# Basic CRUD template

User CRUD Template the I use as a start for a Flask App.  

Running this app:  
git clone this app to the server and in the folder created, create the following file:  
mkdir .env  

Add the following contents
>PYTHON_VERSION=3.10.8  
APP_NAME=Application name  
APP_DESCRIPTION=Application description  
USE_POSTGRES=0  
POSTGRES_USER=webapp  
POSTGRES_PASSWORD=passmedb  
POSTGRES_DB=webapp  
POSTGRES_SERVER=localhost  
FLASK_DEBUG=1  
FLASK_ENV=development  
FLASK_RUN_HOST=0.0.0.0  
GUNICORN_WORKERS=1  
LOG_LEVEL=debug  
SECRET_KEY=not-so-secret  
CRYPT_KEY=fiujwefiwefbweifbiewbfiewb  
EMAIL_USER=<your@email.address>  
EMAIL_PASSWORD=email_pass  

Python version 3.10+ required  

Run the following:  

python -m venv .venv  
.venv/bin/activate  
pip install --upgrade setuptools  
pip install --upgrade pip  
pip install environs  
pip install -e .  

Test run with:  
flask run  
