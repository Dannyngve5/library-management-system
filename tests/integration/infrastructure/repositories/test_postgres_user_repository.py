from domain.entities.user import User, UserRole

from config.settings import (
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_PORT,
    POSTGRES_TEST_DB,
    POSTGRES_USER,
)
from infrastructure.database.postgres_database import PostgresDatabase
from infrastructure.repositories.postgres.postgres_user_repository import (
    PostgresUserRepository,
)


def test_insert_and_find_user():

    database = PostgresDatabase(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_TEST_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )

    connection = database.get_connection()

    repository = PostgresUserRepository(connection)

    user = User(
        user_id=None,
        name="Integration Test User",
        role=UserRole.STUDENT,
    )

    created_user = repository.insert(user)

    found_user = repository.find_by_id(created_user.user_id)

    assert found_user.user_id == created_user.user_id
    assert found_user.name == created_user.name
    assert found_user.role == created_user.role

    connection.rollback()
    connection.close()
