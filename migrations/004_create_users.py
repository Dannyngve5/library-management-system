NAME = "004_create_users"


def up(connection):
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL CHECK(length(trim(name)) > 0),
        role TEXT NOT NULL
            CHECK (role IN ('student', 'professor'))
    )
    """)
