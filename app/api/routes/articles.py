from fastapi import APIRouter, HTTPException, Query
from app.schemas.article import ArticlePublic, ArticleCreate
from app.services.article_service import create_article
from app.deps import SessionDep
from app.models.article import Article
from sqlmodel import select
from typing import List

router = APIRouter()

@router.post("/", response_model=ArticlePublic)
def create_new_article(article: ArticleCreate, db: SessionDep):
    existing_article = db.query(Article).filter(Article.title == article.title).first()
    if existing_article:
        raise HTTPException(status_code=400, detail="Article with this title already exists")

    db_article = create_article(db, article)
    return db_article

@router.get("/", response_model=List[ArticlePublic])
def list_articles(
    db: SessionDep,
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of items to return")
):
    articles = db.exec(select(Article).offset(skip).limit(limit)).all()
    return articles
