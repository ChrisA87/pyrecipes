import click
import re
from colorama import Fore, init
from pyrecipes.cookbook import cookbook

init(autoreset=True)

COLOURS = {
    "black": Fore.BLACK,
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
    "none": Fore.RESET,
}


def render_match(pattern, line_number, line, chapter, number, color=Fore.RED):
    click.echo(f"Recipe: {chapter}.{number}, line: {line_number}")
    click.echo(re.sub(re.compile(pattern), color + pattern + Fore.RESET, line))


@click.command()
@click.argument("pattern", type=str)
@click.option(
    "-c",
    "--color",
    type=click.Choice(COLOURS.keys(), case_sensitive=False),
    default="red",
)
def search(pattern, color):
    """Search the recipes for a pattern"""
    for _, chapter in cookbook:
        for _, recipe in chapter:
            matches = recipe.search(pattern)
            if matches:
                for match in matches:
                    render_match(pattern, *match, COLOURS.get(color.lower(), "red"))
