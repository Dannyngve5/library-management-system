import pytest

from config.settings import (
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_TEST_HOST,
    POSTGRES_TEST_DB,
    POSTGRES_USER,
)
from infrastructure.database.postgres_database import PostgresDatabase


@pytest.fixture
def clean_postgres_database():

    database = PostgresDatabase(
        host=POSTGRES_TEST_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_TEST_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )

    connection = database.get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        TRUNCATE TABLE
            loans,
            copies,
            users,
            books
        RESTART IDENTITY CASCADE
        """)

    connection.commit()
    connection.close()

    yield

    connection = database.get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        TRUNCATE TABLE
            loans,
            copies,
            users,
            books
        RESTART IDENTITY CASCADE
        """)

    connection.commit()
    connection.close()
