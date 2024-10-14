.ONESHELL:

run:
	make build
	python out/bundle.py -OO

build:
	make format
	make virtualenv
	python tinyBundle.py -OO

virtualenv:
ifeq ($(OS),Windows_NT)
	.\venv\Scripts\activate
else
	source venv/bin/activate
endif

format:
	ruff check --fix src/ --config ruff.toml
	ruff format src/ --config ruff.toml

setup: requirements.txt
	python -m pip install --user virtualenv
	virtualenv venv
	make virtualenv
	make pip
	python --version

pip: requirements.txt
	python -m pip install -r requirements.txt --no-color