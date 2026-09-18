import psycopg
from psycopg import sql

from config.settings import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_TEST_DB,
    POSTGRES_USER,
)
from infrastructure.migrations.postgres.migration import migrate


def create_database_if_needed() -> None:
    connection = psycopg.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        autocommit=True,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (POSTGRES_TEST_DB,),
            )
            if cursor.fetchone() is None:
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(POSTGRES_TEST_DB)
                    )
                )
    finally:
        connection.close()


if __name__ == "__main__":
    create_database_if_needed()
    migrate(POSTGRES_TEST_DB)
