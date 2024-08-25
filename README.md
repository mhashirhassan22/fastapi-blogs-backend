# Blogs Backend

This project is a FastAPI-based backend for managing a blog application. The application is containerized using Docker and uses PostgreSQL as the database.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Docker
- Docker Compose
- Poetry

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/mhashirhassan22/fastapi-blogs-backend.git
   cd blogs-backend
   ```

2. **Set up the Python environment**:

Install dependencies using Poetry:
    ```bash
    poetry install
    ```
3. **Build and run the Docker containers:**:
Build and start the Docker containers:
    ```bash
    docker-compose up --build
    ```

This command will start both the FastAPI application and the PostgreSQL database.

### Usage
* The FastAPI application will be available at http://localhost:8000.
* API documentation can be accessed via http://localhost:8000/docs for Swagger UI or http://localhost:8000/redoc for ReDoc.

### Running Tests
To run tests, use:
    ```bash
    poetry run pytest
    ```
### Database Migrations
This project uses Alembic for database migrations. To create a new migration, run:
    ```bash
    poetry run alembic revision --autogenerate -m "Migration message"
    ```
To apply migrations, use:
    ```bash
    poetry run alembic upgrade head
    ```
### Packaging
The application is set up to be packaged using Poetry. To build the package, run:
    ```bash
    poetry build
    ```
