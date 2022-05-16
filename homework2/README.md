# HTML page parser

## Launching
First you need to install the required packages:
```
pip install poetry
```
Install Dependencies:
```
poetry install
```
You need to go to repository, activate the virtual environment for the project and run:
```
python3 -m weather city
```
If you want to run the program with PyCharm, then you need to specify in the configuration:
1. write parameters: city
2. click on the button emulate terminal in output console

## Description
The program receives the weather in a particular city. The program supports saving. If the user recognized it within the previous 5 minutes, then this value will be received, without a new request to the site. If an incorrect city name is entered, or the city is not Russian, an error message will be displayed.
You can see the names of the cities on the website:
```
https://world-weather.ru/pogoda/russia/
```
## Testing
To run the tests, you need to go to the repository, activate the virtual environment for the project, and write:
```
pytest -v tests
```