# pylint: disable=missing-module-docstring
import typer

from weather.parse_html import parse


def main(city: str) -> bool:
    """
    Функция выводить текущую погоду в городе city.
    Если название города city некорректно, то
    выводится "Error".
    """
    current_weather = parse(city)
    if current_weather != "Error":
        typer.echo(f"Current weather in {city}: {current_weather}.")
        return True
    typer.echo("Error")
    return False
