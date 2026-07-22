import sqlite3


# Fabrica conexiones
class Database:

    def __init__(self, path):
        self.path = path

    def get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection
