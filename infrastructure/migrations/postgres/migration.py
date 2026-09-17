import importlib

from infrastructure.database.postgres_database import PostgresDatabase
from infrastructure.migrations.postgres.postgres_migration_repository import (
    PostgresMigrationRepository,
)
from config.settings import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)

MIGRATIONS = [
    "001_create_books",
    "002_create_copies",
    "003_create_users",
    "004_create_loans",
]


def migrate(database_name: str = POSTGRES_DB):

    database = PostgresDatabase(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=database_name,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )

    connection = database.get_connection()

    repository = PostgresMigrationRepository(connection)

    repository.create_table()

    for migration_name in MIGRATIONS:

        migration = importlib.import_module(
            f"infrastructure.migrations.postgres.{migration_name}"
        )

        if repository.has_executed(migration.NAME):
            continue

        migration.up(connection)

        repository.register(migration.NAME)

    connection.commit()

    connection.close()


if __name__ == "__main__":
    migrate()
