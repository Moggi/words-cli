#!/usr/bin/env python3

import os
import time
import json
import asyncio
import aiohttp
import aiofiles
from typing import Set, List

RANGE_LIMIT = 500
BASE_FILE_PATH = 'words_definitions/'
BASE_ERROR_PATH = 'words_with_error/'
BASE_URL = 'https://some.pretty.api/words/'
HEADERS = {
    'api-key': "huge-api-key"
}

WORD_LIST_FILE_NAME = 'words_to_search.txt'


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
        async with aiofiles.open(BASE_ERROR_PATH+word, "w") as f:
            await f.write(json.dumps(result))
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


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
