
import json
import click
import requests
from . import configure_env_var

_BASE_URL = 'BASE_URL'


@click.command('login')
@click.option('-b', '--base_url', envvar=_BASE_URL,
              show_default=True, type=str,
              help=f"Base api url (overrides {_BASE_URL} env var).")
@click.argument('output', default='-', type=click.File('w'), required=False)
@click.option('-u', '--username', prompt="Your username",
              help="Username with no blank spaces.")
@click.option('-p', '--password', prompt=True, hide_input=True,
              help="Password with at least 8 characteres.")
@click.pass_context
def initiate_login_session(ctx, base_url, output, username, password):
    """Login to api and save the access token."""
    base_url = configure_env_var(_BASE_URL, base_url)
    URL = f'{base_url}/token/'
    auth = {
        'username': username,
        'password': password
    }
    res = requests.post(URL, data=auth)
    if res.status_code == 200:
        click.echo(json.dumps(res.json()), file=output)
    else:
        click.echo(f'Error code: {res.status_code}')
        click.echo(res.text, file=output)
