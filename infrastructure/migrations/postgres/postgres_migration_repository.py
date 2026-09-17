from datetime import datetime


class PostgresMigrationRepository:

    def __init__(self, connection):
        self.connection = connection

    def create_table(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS migrations(
                migration_name VARCHAR(255) PRIMARY KEY,
                executed_at TIMESTAMP NOT NULL
            )
            """)

    def has_executed(self, migration_name: str) -> bool:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM migrations
            WHERE migration_name = %s
            """,
            (migration_name,),
        )

        return cursor.fetchone() is not None

    def register(self, migration_name: str):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO migrations(
                migration_name,
                executed_at
            )
            VALUES (%s, %s)
            """,
            (
                migration_name,
                datetime.now(),
            ),
        )
