from fastapi import APIRouter

from .routes import articles

api_router = APIRouter()
api_router.include_router(articles.router,prefix="/articles", tags=["articles"])
