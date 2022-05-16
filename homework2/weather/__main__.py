# pylint: disable=missing-module-docstring
import typer

from weather.main_weather import main

if __name__ == '__main__':
    typer.run(main)
