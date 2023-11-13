# Creating virtual environment inside current folder

python3 -m venv .venv

# To run flask, virtual environment needs to be "started" inside the command line

. .venv/bin/activate

or

source .venv/bin/activate


# Running Flask at port 5000 with server file "main.py"

flask --app main run --debug --port 5000