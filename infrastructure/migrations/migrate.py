import importlib

from infrastructure.database.database import Database
from infrastructure.migrations.migration_repository import MigrationRepository

MIGRATIONS = [
    "001_create_books",
    "002_create_copies",
    "003_create_loans",
    "004_create_users",
]


def migrate():

    database = Database("library.db")

    connection = database.get_connection()

    repository = MigrationRepository(connection)

    repository.create_table()

    for migration_name in MIGRATIONS:

        migration = importlib.import_module(
            f"infrastructure.migrations.{migration_name}"
        )

        if repository.has_executed(migration.NAME):
            continue

        migration.up(connection)

        repository.register(migration.NAME)

    connection.commit()

    connection.close()


if __name__ == "__main__":
    migrate()
