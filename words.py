#!/usr/bin/env python3

from dotenv import load_dotenv

load_dotenv(override=True)

if __name__ == '__main__':
    from src import commands
    commands.cli()
