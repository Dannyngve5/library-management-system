# Library Management System

Backend application for managing books, copies, users, loans, and returns.
The project follows a layered architecture inspired by Clean Architecture.

## Active Application

PostgreSQL is the active database. The project has two application interfaces:

- `main.py`: console interface.
- `app.py`: FastAPI interface.

Both interfaces use `config/dependencies.py`, `PostgresUnitOfWork`, and the
PostgreSQL repositories. Apply the PostgreSQL schema before starting either
interface:

Create a local `.env` from `.env.example` and set its PostgreSQL password
before running the commands below.

```powershell
\.venv\Scripts\python.exe -m infrastructure.migrations.postgres.migration
```

Start the console interface:

```powershell
\.venv\Scripts\python.exe main.py
```

Start the API:

```powershell
\.venv\Scripts\python.exe -m uvicorn app:app --reload
```

## SQLite Legacy Implementation

SQLite is retained as the academic implementation of the original version. It
is not used by the active console or API. Its dependency wiring is kept in
`config/dependencies_sqlite.py`; SQLite repositories, unit of work, and schema
migrations remain under the corresponding `infrastructure` folders.

The legacy database file is `sql_library.db`. To migrate its data to
PostgreSQL, create the PostgreSQL schema first and then run:

```powershell
\.venv\Scripts\python.exe scripts\migrate_sqlite_to_postgres.py
```

The migration preserves primary keys and foreign-key relationships, converts
SQLite availability values to PostgreSQL booleans, resets PostgreSQL
sequences, and can be safely repeated because existing rows are updated with
`ON CONFLICT ... DO UPDATE`.

## Architecture and Patterns

- Domain entities and exceptions
- Application services and DTOs
- Repository Pattern
- Unit of Work
- Factory Pattern
- Dependency Injection
- PostgreSQL migrations
- SQLite legacy implementation and migration utility

## Project Structure

- `application/`: services, DTOs, and interfaces
- `domain/`: entities and domain exceptions
- `infrastructure/repositories/postgres/`: active repositories
- `infrastructure/repositories/sqlite/`: legacy repositories
- `infrastructure/migrations/postgres/`: active schema migrations
- `infrastructure/migrations/sqlite/`: legacy schema migrations
- `presentation/`: console and FastAPI interfaces
- `scripts/migrate_sqlite_to_postgres.py`: data transfer utility

## Tests

```powershell
\.venv\Scripts\python.exe -m pytest -q
```
