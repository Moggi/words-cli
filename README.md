
# words-cli

An "working" command line to manage an Word API. Made to learn [Click](https://github.com/pallets/click)

## Dependencies

- Python 3.8
- [Pipenv](https://github.com/pypa/pipenv)

## Configure

- Copy `.env.bkp` to `.env` and change the variables there.

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
