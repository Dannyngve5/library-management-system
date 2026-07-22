NAME = "001_create_books"


def up(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books(
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT NOT NULL UNIQUE CHECK(length(trim(isbn)) > 0),
            title TEXT NOT NULL CHECK(length(trim(isbn)) > 0),
            author TEXT NOT NULL CHECK(length(trim(isbn)) > 0)
        )
    """)
