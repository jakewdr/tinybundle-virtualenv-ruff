# Setup

1) Install [Taskfile](https://taskfile.dev/installation/) for your operating system

2) Make sure the [Python](https://www.python.org/downloads/) version you are going to use for the virtualenv is installed on the system and added to path (this project has been tested on python [3.11.x](https://www.python.org/downloads/release/python-3119/))

3) Install virtualenv using:

    python -m pip install --user virtualenv

Firstly you need to create the virtual environment:

    virtualenv venv

Next you need to activate it (first is for windows second is for unix based):

    .\venv\Scripts\activate
    source venv/bin/activate

Then all you need to do is navigate to the project directory and run:

    task setup

# Running the project

To run the project you can run (make sure the virtual env has been activated):

    task run

If you only want to build the project use:

    task build
