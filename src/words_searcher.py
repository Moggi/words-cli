#!/usr/bin/env python3

import os
import time
import json
import click
import asyncio
import aiohttp
import aiofiles
from typing import Set, List

from . import retrieve_env_var, configure_env_var

_BASE_URL = 'WORD_API_BASE_URL'
BASE_URL = retrieve_env_var(_BASE_URL)
RANGE_LIMIT = int(retrieve_env_var('RANGE_LIMIT', 100))
BASE_FILE_PATH = retrieve_env_var('BASE_FILE_PATH')
BASE_ERROR_PATH = retrieve_env_var('BASE_ERROR_PATH')
HEADERS = {
    retrieve_env_var('WORD_HOST_HEADER'): retrieve_env_var('WORD_API_HOST'),
    retrieve_env_var('WORD_KEY_HEADER'): retrieve_env_var('WORD_API_KEY')
}

WORD_LIST_FILE_NAME = retrieve_env_var('WORD_LIST_FILE_NAME')


@click.command('search')
@click.option('-b', '--base_url', envvar=_BASE_URL,
              show_default=True, type=str,
              help=f'Base api url (overrides {_BASE_URL} env var).')
@click.argument('output', default='-', type=click.File('w'), required=False)
def words_searcher(base_url, output):
    """Bulk search all words from the {WORD_LIST_FILE_NAME}."""
    configure_env_var(_BASE_URL, base_url)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()


async def main():
    t0 = time.time()
    task1 = asyncio.create_task(get_words_from_file(WORD_LIST_FILE_NAME))
    task2 = asyncio.create_task(get_words_from_dir(BASE_FILE_PATH))
    task3 = asyncio.create_task(get_words_from_dir(BASE_ERROR_PATH))
    # @TODO: Improve this tasks time. It is taking too long.
    await asyncio.wait([task1, task2, task3])
    t1 = time.time()

    words_new: set = task1.result()
    words_saved: set = task2.result()
    words_with_error: set = task3.result()
    print(len(words_new), end=' comming words\n')
    print(len(words_saved), end=' saved words\n')
    print(len(words_with_error), end=' error words\n')

    words = list(words_new.difference(words_saved.union(words_with_error)))

    print(len(words), end=' new words\n')

    await asyncio.wait_for(
            bulk_fetch_and_write(words=words[:RANGE_LIMIT]), timeout=60*60)

    tn = time.time()
    print('Time on first task: {:.2f}s'.format(t1-t0))
    print('Time on second task: {:.2f}s'.format(tn-t1))
    print('Total time spent: {:.2f}s'.format(tn-t0))


async def get_words_from_dir(base_path: str) -> Set:
    """Retrieve word list from file names on a given directory."""
    await asyncio.sleep(10/1000)
    return set(os.listdir(base_path))


async def get_words_from_file(file_name: str) -> Set:
    """Retrieve word list from a given file name. One per line."""
    words = set()
    async with aiofiles.open(file_name, 'r') as f:
        async for line in f:
            word = line.strip()
            if word:
                words.add(word)
    return words


async def fetch_url(session, url) -> dict:
    """Fetch an url with the global headers."""
    async with session.get(url, headers=HEADERS) as response:
        return await response.json()


async def write_one(word: str, session) -> None:
    """Asyncronosly write to a file the contents of the `BASE_URL+word` url."""
    try:
        result = await fetch_url(session=session, url=BASE_URL+word)
        if result is None or 'word' not in result:
            raise Exception(f' ==# Error on word: {word}')
        async with aiofiles.open(BASE_FILE_PATH+word, "w") as f:
            await f.write(json.dumps(result))
    except Exception as e:
        print(f'{e}')
        try:
            async with aiofiles.open(BASE_ERROR_PATH+word, "w") as f:
                await f.write(json.dumps(result))
        finally:
            return None


async def bulk_fetch_and_write(words: List) -> None:
    """Fetch and write concurrently for multiple words."""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for word in words:
            tasks.append(
                write_one(word=word, session=session)
            )
        await asyncio.gather(*tasks)
