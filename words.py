#!/usr/bin/env python3

from src import commands, configure_env_var

_BASE_URL = 'BASE_URL'
BASE_URL = 'https://you.pretty/api'


if __name__ == '__main__':
    configure_env_var(_BASE_URL, BASE_URL)
    commands.cli()
