from sqlmodel import Session
from app.models.article import Article
from fastapi import HTTPException, status
from sqlmodel import select
from app.schemas.article import ArticleCreate, ArticleUpdate

def create_article(db: Session, article_create: ArticleCreate) -> Article:
    new_article = Article.model_validate(article_create)
    db.add(new_article)
    db.commit()
    db.refresh(new_article) # auto gen id
    return new_article

def delete_article_by_id(db: Session, id: int):
    statement = select(Article).where(Article.id == id)
    article = db.exec(statement).first()

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    db.delete(article)
    db.commit()

def update_article_by_id(db: Session, id: int, article_update: ArticleUpdate) -> Article:
    statement = select(Article).where(Article.id == id)
    article = db.exec(statement).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    update_data = article_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(article, key, value)

    db.add(article)
    db.commit()
    db.refresh(article)
    return article
