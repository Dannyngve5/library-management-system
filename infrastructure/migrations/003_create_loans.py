NAME = "003_create_loans"


def up(connection):
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS loans(
        loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        copy_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,

        start_date DATE NOT NULL,
        due_date DATE NOT NULL
            CHECK (due_date >= start_date),

        returned_date DATE
            CHECK (
                returned_date IS NULL
                OR returned_date >= start_date
            ),

        FOREIGN KEY (copy_id)
            REFERENCES copies(copy_id)
            ON DELETE RESTRICT,

        FOREIGN KEY (user_id)
            REFERENCES users(user_id)
            ON DELETE RESTRICT
    )
    """)
