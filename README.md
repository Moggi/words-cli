
# words-cli

An "working" command line to manage an Word API. Made to learn [Click][1]

## Dependencies

- [Python 3.8][2]
- [Pipenv][3]

## Configure

- Copy `.env.bkp` to `.env` and change the variables there.
- Create the `BASE_FILE_PATH` and `BASE_ERROR_PATH` directories
- Create your `WORD_LIST_FILE_NAME` file and insert one word by line

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

[1]: https://github.com/pallets/click
[2]: https://www.python.org/downloads/
[3]: https://github.com/pypa/pipenv
