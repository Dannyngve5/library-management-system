from datetime import datetime
import sqlite3


class MigrationRepository:

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def create_table(self):
        cursor = self.connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS migrations(
                migration_name TEXT PRIMARY KEY,
                executed_at TEXT NOT NULL
            )
        """)

    def has_executed(self, migration_name: str) -> bool:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT 1
            FROM migrations
            WHERE migration_name = ?
            """,
            (migration_name,),
        )

        return cursor.fetchone() is not None

    def register(self, migration_name: str):
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO migrations(migration_name, executed_at)
            VALUES (?, ?)
            """,
            (migration_name, datetime.now().isoformat()),
        )
