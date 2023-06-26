# Phone Manager

Used to set configs for snom and yealink endpoints.  
Phone gets a IP/DNS from our DHCP server. The DNS server must by ours.  
We modify the DNS server entry for snom/yealink domains to point to our config server.  

When the phone requests a config from the snom/yealink server, our server will complete te request.  

Running this app:  
git clone this app to the server and in the folder created, create the following file:  
mkdir .env  

Add the following contents
>PYTHON_VERSION=3.10.8  
APP_NAME=Phone Manager  
APP_DESCRIPTION=Management app for SNOM and Yealink IP Phones  
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
EMAIL_USER=your@email.address  
EMAIL_PASSWORD=test`  

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
