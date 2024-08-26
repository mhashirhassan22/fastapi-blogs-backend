from sqlmodel import Session
from app.models.article import Article
from app.schemas.article import ArticleCreate

def create_article_in_db(session: Session, article_in: ArticleCreate) -> Article:
    article = Article.model_validate(article_in)
    session.add(article)
    session.commit()
    session.refresh(article)
    return article
