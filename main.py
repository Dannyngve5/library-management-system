from infrastructure.migrations.postgres.migration import migrate
from presentation.console.menu import Menu

from config.dependencies import (
    library_service,
    user_service,
    loan_service,
)

if __name__ == "__main__":

    migrate()

    menu = Menu(
        library_service,
        user_service,
        loan_service,
    )

    menu.show()
