import click
import sys
# строчку ниже поменять
sys.path.insert(0, '/Users/aleksandrskiba/Documents/python_kib_project/client')
# строчку выше поменять
from client import ClientError, Send, auth_reg, sending, main


@click.group()
def cli():
    """Command line interface"""


@click.command('start')
def work():
    click.echo('Start working english app')
    main()
cli.add_command(work)
cli()