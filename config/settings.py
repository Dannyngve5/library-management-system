import os

from dotenv import load_dotenv

load_dotenv()


def _required_setting(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


POSTGRES_HOST = _required_setting("POSTGRES_HOST")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = _required_setting("POSTGRES_DB")
POSTGRES_TEST_DB = os.getenv("POSTGRES_TEST_DB", "library_postgres_test")
POSTGRES_USER = _required_setting("POSTGRES_USER")
POSTGRES_PASSWORD = _required_setting("POSTGRES_PASSWORD")
