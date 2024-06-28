.ONESHELL:

run:
	make build
	python out/bundle.py -OO

build:
	make venv
	make format
	python tinyBundle.py -OO

venv:
	ifeq ($(OS),Windows_NT)
		venv/Scripts/activate
	endif
	ifeq ($(UNAME_S),Linux)
		source venv/Scripts/activate
	endif

format:
	make venv
	ruff check --fix src/ --config ruff.toml
	ruff format src/ --config ruff.toml

debug:
	make venv
	ruff check src/ --config ruff.toml
	python -m pdb src/__main__.py

setup: requirements.txt
	python -m venv venv
	make venv
	make pip

pip: requirements.txt
	python -m pip install -r requirements.txt --no-color