
import os
import time
import click
import asyncio
import aiohttp
import aiofiles
from typing import Set, List

from . import retrieve_env_var, configure_env_var

_BASE_URL = 'BASE_URL'
_ACCESS_TOKEN = 'ACCESS_TOKEN'
BASE_FILE_PATH = 'words_definitions/'
RANGE_LIMIT = 200


@click.command('bulk_upload')
@click.option('-b', '--base_url', envvar=_BASE_URL,
              show_default=True, type=str,
              help=f'Base api url (overrides {_BASE_URL} env var).')
@click.argument('output', default='-', type=click.File('w'), required=False)
def bulk_upload(base_url, output):
    """Bulk upload all already saved words to the server."""
    configure_env_var(_BASE_URL, base_url)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()


async def main():
    t0 = time.time()
    task1 = asyncio.create_task(get_words_from_server())
    task2 = asyncio.create_task(get_words_from_dir(BASE_FILE_PATH))
    await asyncio.wait([task1, task2])
    t1 = time.time()

    words_server: set = task1.result()
    words_local: set = task2.result()
    click.echo(f'{len(words_local)} local words')
    click.echo(f'{len(words_server)} words on server')

    words = list(words_local.difference(words_server))

    click.echo(f'{len(words)} new words to upload')

    await asyncio.wait_for(
            bulk_fetch_and_write(words=words[:RANGE_LIMIT]), timeout=60*60)

    tn = time.time()
    click.echo('Time on first task: {:.2f}s'.format(t1-t0))
    click.echo('Time on second task: {:.2f}s'.format(tn-t1))
    click.echo('Total time spent: {:.2f}s'.format(tn-t0))


def retrieve_headers():
    ACCESS_TOKEN = retrieve_env_var(_ACCESS_TOKEN)
    return {
        'Accept': 'application/json',
        # 'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }


async def get_words_from_server() -> Set:
    """Retrieve word list from server."""
    BASE_URL = retrieve_env_var(_BASE_URL)
    URL = f'{BASE_URL}/words/'
    HEADERS = retrieve_headers()
    words = set()
    async with aiohttp.ClientSession() as client:
        async with client.get(URL, headers=HEADERS) as res:
            if res.status != 200:
                raise Exception(f'Error {res.status} on listing from server.')
            for word in await res.json():
                words.add(word['name'])
            return words


async def get_words_from_dir(base_path: str) -> Set:
    """Retrieve word list from file names on a given directory."""
    await asyncio.sleep(10/1000)
    return set(os.listdir(base_path))


async def retrieve_word_data(word) -> str:
    """Fetch ."""
    async with aiofiles.open(BASE_FILE_PATH+word) as file:
        return await file.read()


async def send_one(word: str, session: aiohttp.ClientSession) -> None:
    """Asyncronosly upload to the server the contents of the word."""
    BASE_URL = retrieve_env_var(_BASE_URL)
    URL = f'{BASE_URL}/words/'
    HEADERS = retrieve_headers()
    try:
        result = await retrieve_word_data(word=word)
        data = {
            'name': word,
            'data': result
        }
        await asyncio.sleep(100/1000)
        async with session.post(URL, data=data, headers=HEADERS) as res:
            if res.status != 201:
                click.echo(await res.text())
                raise Exception(f'Error {res.status} on word {word}\n{res}')
    except Exception as e:
        click.echo(f'{e}')


async def bulk_fetch_and_write(words: List) -> None:
    """Fetch and write concurrently for multiple words."""
    conn = aiohttp.BaseConnector(limit=5, limit_per_host=5)
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = []
        for word in words:
            tasks.append(
                send_one(word=word, session=session)
            )
        await asyncio.gather(*tasks)
