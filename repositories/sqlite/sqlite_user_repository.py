from repositories.interfaces.iuser_repository import IUserRepository
from models.user import User, UserRole


class SqliteUserRepository(IUserRepository):

    def __init__(self, connection):
        self.connection = connection

    def insert(self, user: User) -> User:
        cursor = self.connection.cursor()

        cursor.execute(
            """
        INSERT INTO users(name, role)
        VALUES (?,?)
        """,
            (user.name, user.role.value),
        )
        user.user_id = cursor.lastrowid
        return user

    def find_by_id(self, user_id: int) -> User | None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
        SELECT *
        FROM users
        WHERE user_id = ?
        """,
            (user_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return User.from_row(row)

    def find_all(self) -> list[User]:
        cursor = self.connection.cursor()

        cursor.execute("""
        SELECT *
        FROM users
        """)

        rows = cursor.fetchall()

        return [User.from_row(row) for row in rows]

    def find_by_role(self, role: UserRole) -> list[User]:
        cursor = self.connection.cursor()

        cursor.execute(
            """
        SELECT *
        FROM users
        WHERE role = ?
        """,
            (role.value,),
        )

        rows = cursor.fetchall()

        return [User.from_row(row) for row in rows]

    def find_by_name(self, name: str) -> list[User]:
        pass

    def update(self, user: User) -> None:
        pass
