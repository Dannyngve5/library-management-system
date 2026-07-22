from infrastructure.migrations.migrate import migrate
from presentation.console.menu import Menu

from config.dependencies import (
    uow,
    library_service,
    user_service,
    loan_service,
)

if __name__ == "__main__":

    migrate()

    # seed_database(uow)  # LOADING SEED DATA

    menu = Menu(
        library_service,
        user_service,
        loan_service,
    )

    menu.show()
