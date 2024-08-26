import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy_utils import create_database, drop_database, database_exists
from sqlmodel import SQLModel, Session
from fastapi.testclient import TestClient
from collections.abc import Generator
from app.main import app
from app.deps import get_db

# Test database URL
TEST_DATABASE_URL = "postgresql://postgres:postgres@db:5432/blogs_backend_test"

# Create engine for the test database
test_engine = create_engine(TEST_DATABASE_URL)

def override_get_db() -> Generator[Session, None, None]:
    with Session(test_engine) as session:
        yield session

# Override the get_db dependency with the test database
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """
    This fixture creates the test database, sets up the schema,
    and drops the database after the tests.
    """
    try:
        # Check if the database exists and create it if it doesn't
        if not database_exists(test_engine.url):
            create_database(test_engine.url)
        # Create tables
        SQLModel.metadata.create_all(test_engine)
        yield
    finally:
        # Drop the test database after the test session
        if database_exists(test_engine.url):
            drop_database(test_engine.url)

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    """
    Fixture to provide a TestClient for making HTTP requests to the FastAPI app.
    """
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def session() -> Generator[Session, None, None]:
    """
    Fixture to provide a database session for the test module.
    """
    with Session(test_engine) as session:
        yield session

@pytest.fixture(autouse=True)
def cleanup_database(session: Session):
    """
    Fixture to clean up the database before each test runs to ensure test isolation.
    """
    yield
    # Clean up the tables to ensure no data leaks between tests
    session.execute(text("TRUNCATE TABLE articles RESTART IDENTITY CASCADE;"))
    session.commit()
