
# words-cli

An "working" command line to manage an Word API. Made to learn [Click](https://github.com/pallets/click)

## Dependencies

- Python 3.8
- [Pipenv](https://github.com/pypa/pipenv)

## Configure

- Open words.py and change the `BASE_URL` variable to match your api
- Then change `BASE_URL` and `HEADERS` on words_searcher.py to match your foreign api

## Run

```sh
# Install deps
python3.8 -m pipenv shell
pipenv sync -d

# Start using
./words.py --help
# ./words.py login -u <username>
# ./words.py list
```
