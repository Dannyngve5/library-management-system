NAME = "002_create_copies"


def up(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS copies(
            copy_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            available INTEGER NOT NULL DEFAULT 1,

            FOREIGN KEY(book_id)
                REFERENCES books(book_id)
        )
    """)
