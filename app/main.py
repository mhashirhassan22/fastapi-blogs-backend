from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from app.api.main import api_router
from app.core.config import settings
from app.middleware.logging import LogRequestMiddleware
from app.core.db import engine, wait_for_database, run_migrations

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for managing blog articles",
    version="1.0.0",
)
app.add_middleware(LogRequestMiddleware) # For request logging

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

def run():
    # getting the database ready
    wait_for_database(engine)
    if settings.ENVIRONMENT == "local":
        # make sure migrations are updated everytime during development
        run_migrations()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    run()
