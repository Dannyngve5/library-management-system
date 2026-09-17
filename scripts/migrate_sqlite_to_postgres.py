import sqlite3

import psycopg

from config.settings import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_USER,
)

SQLITE_DATABASE = "sql_library.db"

POSTGRES_CONFIG = {
    "host": POSTGRES_HOST,
    "port": POSTGRES_PORT,
    "dbname": POSTGRES_DB,
    "user": POSTGRES_USER,
    "password": POSTGRES_PASSWORD,
}


def migrate():
    sqlite_connection = sqlite3.connect(SQLITE_DATABASE)
    postgres_connection = psycopg.connect(**POSTGRES_CONFIG)

    try:
        migrate_books(
            sqlite_connection,
            postgres_connection,
        )

        migrate_copies(
            sqlite_connection,
            postgres_connection,
        )

        migrate_users(
            sqlite_connection,
            postgres_connection,
        )

        migrate_loans(
            sqlite_connection,
            postgres_connection,
        )

        reset_sequences(postgres_connection)

        postgres_connection.commit()

    except Exception:
        postgres_connection.rollback()
        raise

    finally:
        sqlite_connection.close()
        postgres_connection.close()


def migrate_books(
    sqlite_connection,
    postgres_connection,
):
    sqlite_cursor = sqlite_connection.cursor()
    postgres_cursor = postgres_connection.cursor()

    sqlite_cursor.execute("""
        SELECT
            book_id,
            isbn,
            title,
            author
        FROM books
        ORDER BY book_id
        """)

    rows = sqlite_cursor.fetchall()

    for row in rows:
        postgres_cursor.execute(
            """
            INSERT INTO books(
                book_id,
                isbn,
                title,
                author
            )
            VALUES (%s, %s, %s, %s)
            """,
            row,
        )


def migrate_copies(
    sqlite_connection,
    postgres_connection,
):
    sqlite_cursor = sqlite_connection.cursor()
    postgres_cursor = postgres_connection.cursor()

    sqlite_cursor.execute("""
        SELECT
            copy_id,
            book_id,
            available
        FROM copies
        ORDER BY copy_id
        """)

    rows = sqlite_cursor.fetchall()

    for row in rows:
        copy_id, book_id, available = row

        postgres_cursor.execute(
            """
            INSERT INTO copies(
                copy_id,
                book_id,
                available
            )
            VALUES (%s, %s, %s)
            """,
            (
                copy_id,
                book_id,
                bool(available),
            ),
        )


def migrate_users(
    sqlite_connection,
    postgres_connection,
):
    sqlite_cursor = sqlite_connection.cursor()
    postgres_cursor = postgres_connection.cursor()

    sqlite_cursor.execute("""
        SELECT
            user_id,
            name,
            role
        FROM users
        ORDER BY user_id
        """)

    rows = sqlite_cursor.fetchall()

    for row in rows:
        postgres_cursor.execute(
            """
            INSERT INTO users(
                user_id,
                name,
                role
            )
            VALUES (%s, %s, %s)
            """,
            row,
        )


def migrate_loans(
    sqlite_connection,
    postgres_connection,
):
    sqlite_cursor = sqlite_connection.cursor()
    postgres_cursor = postgres_connection.cursor()

    sqlite_cursor.execute("""
        SELECT
            loan_id,
            copy_id,
            user_id,
            start_date,
            due_date,
            returned_date
        FROM loans
        ORDER BY loan_id
        """)

    rows = sqlite_cursor.fetchall()

    for row in rows:
        postgres_cursor.execute(
            """
            INSERT INTO loans(
                loan_id,
                copy_id,
                user_id,
                start_date,
                due_date,
                returned_date
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            row,
        )


def reset_sequences(postgres_connection):
    postgres_cursor = postgres_connection.cursor()

    for table, column in [
        ("books", "book_id"),
        ("copies", "copy_id"),
        ("users", "user_id"),
        ("loans", "loan_id"),
    ]:
        postgres_cursor.execute(f"""
            SELECT setval(
                pg_get_serial_sequence(
                    '{table}',
                    '{column}'
                ),
                COALESCE(
                    (
                        SELECT MAX({column})
                        FROM {table}
                    ),
                    1
                )
            )
            """)


if __name__ == "__main__":
    migrate()
