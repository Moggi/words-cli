
import json
import click
import requests

from . import retrieve_env_var, configure_env_var

_BASE_URL = 'BASE_URL'
_ACCESS_TOKEN = 'ACCESS_TOKEN'


@click.command('list')
@click.option('-b', '--base_url', envvar=_BASE_URL,
              show_default=True, type=str,
              help=f"Base api url (overrides {_BASE_URL} env var).")
@click.argument('output', default='-', type=click.File('w'), required=False)
def words_list(base_url, output):
    """Retrieve a list of all words on the server."""
    base_url = configure_env_var(_BASE_URL, base_url)
    url = f'{base_url}/words/all/'
    headers = retrieve_headers()
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        click.echo(json.dumps(res.json()), file=output)
    else:
        click.echo(f'Error code: {res.status_code}')
        click.echo(res.text, file=output)


def retrieve_headers():
    ACCESS_TOKEN = retrieve_env_var(_ACCESS_TOKEN)
    return {
        'Accept': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
