from sqlmodel import create_engine
from app.core.config import settings
from app.models.article import Article
import time
from sqlalchemy.exc import OperationalError
import subprocess
from sqlalchemy_utils import database_exists, create_database

def create_database_if_not_exists(engine):
    """
    Create the database if it doesn't exist.
    """
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Database created at {engine.url}")
    else:
        print(f"Database already exists at {engine.url}")



def run_migrations():
    """
    Run Alembic migrations to ensure the database schema is up to date.
    """
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Migrations applied successfully.")
    except subprocess.CalledProcessError:
        print("Failed to apply migrations.")
        raise

def wait_for_database(engine, timeout=30):
    """
    Wait for the database to be ready.
    """
    start_time = time.time()
    try_db_init = False
    while True:
        try:
            print(f"dabatabase url {engine.url}")
            connection = engine.connect()
            connection.close()
            print("Database is ready.")
            break
        except OperationalError:
            if time.time() - start_time > timeout:
                raise Exception("Could not connect to the database within the timeout period.")
            if not try_db_init:
                print("Creating database if it does not exist already")
                create_database_if_not_exists(engine)
                try_db_init = True
            print("Database is not ready, waiting...")
            time.sleep(2)

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
