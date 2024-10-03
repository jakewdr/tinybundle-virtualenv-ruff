.ONESHELL:

PYTHON=${VENV_NAME}/bin/python

run:
	make build
	${PYTHON} out/bundle.py -OO

build:
	make format
	${PYTHON} tinyBundle.py -OO

venv:
	ifeq ($(OS),Windows_NT)
		venv/Scripts/activate
	endif
	ifeq ($(UNAME_S),Linux)
		source venv/Scripts/activate
	endif

format:
	ruff check --fix src/ --config ruff.toml
	ruff format src/ --config ruff.toml

setup: requirements.txt
	${PYTHON} -m venv venv
	make venv && make pip && ${PYTHON} --version

pip: requirements.txt
	${PYTHON} -m pip install -r requirements.txt --no-color