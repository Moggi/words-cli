
import os
from dotenv import load_dotenv

load_dotenv(override=False)

DEBUG = os.getenv('DEBUG', False)
VERBOSE = os.getenv('VERBOSE', False)

BASE_API_URL = os.getenv('BASE_API_URL')

WORD_API_BASE_URL = os.getenv('WORD_API_BASE_URL')
WORD_API_HOST = os.getenv('WORD_API_HOST')
WORD_API_KEY = os.getenv('WORD_API_KEY')

RANGE_LIMIT = os.getenv('RANGE_LIMIT', 100)
