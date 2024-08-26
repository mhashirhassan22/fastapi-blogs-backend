from sqlmodel import Session
from app.models.article import Article
from app.schemas.article import ArticleCreate

def create_article(db: Session, article_create: ArticleCreate) -> Article:
    new_article = Article.from_orm(article_create)
    db.add(new_article)
    db.commit()
    db.refresh(new_article) # auto gen id
    return new_article
