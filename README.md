# Basic CRUD template

User CRUD Template that I use as a start for a Flask App.  
CSS in Bootstrap to keep it simple.  

Running this app:  
git clone this app and in the folder created, create the following file:  
vi .env  

Add the following contents
>PYTHON_VERSION=3.10.8  
APP_NAME=Application name  
APP_DESCRIPTION=Application description  
USE_POSTGRES=0  
POSTGRES_USER=webapp  
POSTGRES_PASSWORD=passmedb  
POSTGRES_DB=webapp  
POSTGRES_SERVER=localhost  
POSTGRES_PORT=5432
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

```bash
cd CRUD-Template
python3 -m venv .venv  
source venv/bin/activate  
pip install --upgrade setuptools  
pip install --upgrade pip  
pip install --upgrade wheel  
pip install environs  
pip install -e .  
```

Test run with:  

```bash
flask create-database  
flask run
```  

Connect to the example site with: <http://127.0.0.1:5000>  
Username: <admin@example.com>  
Password: password123

### Running on Docker

1. Create a build from present Dockerfile in this project

```bash
docker build --tag python-docker .
```

2. Run Docker container created on step 1

```bash
docker run -d -p 5000:5000 python-docker
```

Connect to the example site with: <http://127.0.0.1:5000>  
Username: <admin@example.com>  
Password: password123  
