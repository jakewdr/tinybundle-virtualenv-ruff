.ONESHELL:

run:
	make build
	python out/bundle.py -OO

build:
	make venv
	make format
	python tinyBundle.py -OO

venv:
	venv/Scripts/activate

format:
	make venv
	ruff check --fix src/ --config ruff.toml
	ruff format src/ --config ruff.toml

setup:
	python -m venv venv # you change the python version as you need
	make venv
	python -m pip install -r requirements.txt --no-color