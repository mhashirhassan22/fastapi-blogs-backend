FROM python:3.11-slim

# Set environment variables
ENV POETRY_VERSION=1.6.1

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files to the container
COPY pyproject.toml poetry.lock /app/

# Install the dependencies
RUN poetry install --no-dev --no-root

# Copy the rest of the application code
COPY . /app

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run the FastAPI server using Uvicorn
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
