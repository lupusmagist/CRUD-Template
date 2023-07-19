FROM python:3.10-slim-buster

WORKDIR /python-docker

COPY setup.py setup.py
COPY .env .env
RUN pip3 install --upgrade setuptools wheel pip environs
RUN pip3 install -e .

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"] 
