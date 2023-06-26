include .env

venv-install:
	pyenv install -s $(PYTHON_VERSION); \
	pyenv local $(PYTHON_VERSION); \
	python -m venv .venv; \
	. .venv/bin/activate; \
	pip install --upgrade setuptools; \
	pip install --upgrade pip; \
	pip install environs; \
	pip install -e .; \

venv-install_test:
	. .venv/bin/activate; \
		pip install pytest

venv-test: install_test
	. .venv/bin/activate; nosetests project/test

venv-clean:
	rm -rf .venv
	find -iname "*.pyc" -delete