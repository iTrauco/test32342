import click
from gcp_cli_tool.commands.hello import hello

@click.group()
def cli():
    """A simple CLI tool."""
    pass

@cli.command()
def greet():
    """Greet the user."""
    hello()

if __name__ == "__main__":
    cli()
