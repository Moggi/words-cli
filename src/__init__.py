
import os


def configure_env_var(NAME: str, value: str, DEFAULT=None):
    value = value if value is not None else os.getenv(NAME, DEFAULT)
    os.environ[NAME] = value
    return value


def retrieve_env_var(NAME: str, DEFAULT=None):
    return os.getenv(NAME, DEFAULT)
