# ToDo

## Launching
First you need to install the required packages:
```
pip install poetry
```
Install Dependencies:
```
poetry install
```
You need to go to repository, activate the virtual environment for the project and:
```
cd app
flask run
```

Also you can use make.
## Description
The program is a web service ToDo. The task in the list is its description. It may or may not be done. The home page displays all tasks. 
The user can only view completed, active, and all tasks. Также присутствует логирование. There is also logging. Logs are stored in logs.log.
## Testing
To run the tests, you need to go to the repository, activate the virtual environment for the project, and write:
```
pytest -v tests
```