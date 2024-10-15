# Flask Set Up

## Using Git Bash for creating an environment
- python -m venv .venv
- . .venv/Scripts/activate
- deactivate

## Optional Dependencies
- pip install python-dotenv
- pip install watchdog

## Install Flask
- pip install Flask

## Run Flask
1. flask --app <main_file_name> run
2. flask run 
    - if the file is named app.py
3. flask run --debug 
    - to activate debug mode
4. flask --app kwizz run --debug 
    - using application factory

## Generate good secret keys
-  python -c 'import secrets; print(secrets.token_hex())'

## Initialize the Database File
- flask --app <database_name> init-db

## Make the Project Installable
- pip install -e .

## Test Coverage
- pip install pytest coverage