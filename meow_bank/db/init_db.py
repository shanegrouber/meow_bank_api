from meow_bank.core.logging import log

from .database import init_db

if __name__ == "__main__":
    log.info("Initializing database...")
    init_db()
    log.info("Database initialized successfully!")
