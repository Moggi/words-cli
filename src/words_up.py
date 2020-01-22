
import json
import click
import requests

from . import retrieve_env_var, configure_env_var

_BASE_URL = 'BASE_URL'
_ACCESS_TOKEN = 'ACCESS_TOKEN'
BASE_FILE_PATH = 'words_definitions/'


@click.command('upload')
@click.option('-b', '--base_url', envvar=_BASE_URL,
              show_default=True, type=str,
              help=f'Base api url (overrides {_BASE_URL} env var).')
@click.argument('word', type=str)
@click.argument('output', default='-', type=click.File('w'), required=False)
def words_up(base_url, word, output):
    """Upload an already saved [word] to the server."""
    base_url = configure_env_var(_BASE_URL, base_url)
    url = f'{base_url}/words/'
    headers = retrieve_headers()

    try:
        word_data = retrieve_word_data(word)
        data = {
            'name': word,
            'data': word_data
        }
        res = requests.post(url, data=data, headers=headers)
        if res.status_code == 201:
            click.echo(json.dumps(res.json()), file=output)
        else:
            raise Exception(f'Error code: {res.status_code}\n{res.text}')
    except Exception as e:
        click.echo(f'{e}', file=output)


def retrieve_word_data(word: str) -> str:
    data = ''
    if not word:
        raise Exception(f'Not valid word: {word}')
    with open(BASE_FILE_PATH+word, 'r') as f:
        data = f.read()
    if not data:
        raise Exception(f'Not valid word data: {word}')
    return data


def retrieve_headers():
    ACCESS_TOKEN = retrieve_env_var(_ACCESS_TOKEN)
    return {
        'Accept': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
