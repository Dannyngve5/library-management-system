from config.dependencies import uow
from infrastructure.seed import seed_database

if __name__ == "__main__":
    seed_database(uow)
