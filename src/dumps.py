
import os
import click
from dotenv import dotenv_values


@click.command('dumps')
@click.option('--full', default=False, type=bool)
@click.pass_context
def dumps_environment(ctx, full):
    """Dumps environment variables and exit."""
    if full:
        variables = os.environ.keys()
        for key in variables:
            click.echo(f'{key}: {os.getenv(key)}')
    else:
        mapping = dotenv_values()
        for variable in mapping:
            click.echo(f'{variable}: {mapping[variable]}')
