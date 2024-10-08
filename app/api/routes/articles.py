from fastapi import APIRouter, HTTPException, Query, status
from app.schemas.article import ArticlePublic, ArticleCreate, ArticleUpdate
from app.services.article_service import create_article, delete_article_by_id,\
    update_article_by_id
from app.deps import SessionDep
from app.models.article import Article
from sqlmodel import select
from typing import List

router = APIRouter()

@router.post("/", response_model=ArticlePublic)
def create_new_article(article: ArticleCreate, db: SessionDep):
    statement = select(Article).where(Article.title == article.title)
    existing_article = db.exec(statement).first()
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

@router.delete("/{id}/", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_article(id: int, db: SessionDep):
    delete_article_by_id(db=db, id=id)
    return

@router.patch("/{id}/", response_model=ArticlePublic)
def update_article(id: int, article_update: ArticleUpdate, db: SessionDep):
    updated_article = update_article_by_id(db, id, article_update)
    return updated_article

@router.get("/{id}/", response_model=ArticlePublic)
def read_article(id: int, db: SessionDep) -> ArticlePublic:
    statement = select(Article).where(Article.id == id)
    article = db.exec(statement).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
