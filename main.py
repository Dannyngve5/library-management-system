from migrations.migrate import migrate
from seed import seed_database

from database.database import Database
from repositories.sqlite.sqlite_repository_factory import SqliteRepositoryFactory
from services.library_service import LibraryService
from unit_of_work.sqlite_unit_of_work import SqliteUnitOfWork
from presentation.menu import Menu
from services.user_service import UserService
from services.loan_service import LoanService

# gui

import tkinter as tk
from presentation.gui import LibraryGUI

if __name__ == "__main__":

    # 1. Ejecutar migraciones pendientes
    migrate()

    # 2. Construir la aplicación
    database = Database("library.db")

    repository_factory = SqliteRepositoryFactory()

    uow = SqliteUnitOfWork(database, repository_factory)

    # seed_database(uow)  # LOADING SEED DATA

    library_service = LibraryService(uow)
    user_service = UserService(uow)
    loan_service = LoanService(uow)

    menu = Menu(library_service, user_service, loan_service)

    # 3. Iniciar la aplicación por consola
    menu.show()

    # Hacer método str en books, copies, loan, terminar métodos no implementados, implementar loan
