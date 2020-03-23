#!/usr/bin/env python3

from src import settings, commands

if __name__ == '__main__':
    # @FIXME: remove dir(settings) without flake8 warning
    dir(settings)
    commands.cli()
