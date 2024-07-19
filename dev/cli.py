# cli.py

import click
from commands.hello import hello

@click.command()
def cli():
    hello()

if __name__ == '__main__':
    cli()
