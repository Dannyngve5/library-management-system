from application.interfaces.repositories.iuser_repository import IUserRepository
from domain.entities.user import User, UserRole


class PostgresUserRepository(IUserRepository):

    def __init__(self, connection):
        self.connection = connection

    def insert(self, user: User) -> User:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO users(name, role)
            VALUES (%s, %s)
            RETURNING user_id
            """,
            (
                user.name,
                user.role.value,
            ),
        )

        user.user_id = cursor.fetchone()[0]
        return user

    def find_by_id(self, user_id: int) -> User | None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE user_id = %s
            """,
            (user_id,),
        )

        row = cursor.fetchone()
        return User.from_row(row) if row else None

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
            WHERE role = %s
            """,
            (role.value,),
        )

        rows = cursor.fetchall()

        return [User.from_row(row) for row in rows]

    def find_by_name(self, name: str) -> list[User]:
        pass

    def update(self, user: User) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            UPDATE users
            SET
                name = %s,
                role = %s
            WHERE user_id = %s
            """,
            (
                user.name,
                user.role.value,
                user.user_id,
            ),
        )

    def delete(self, user_id: int) -> None:
        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE FROM users
            WHERE user_id = %s
            """,
            (user_id,),
        )
