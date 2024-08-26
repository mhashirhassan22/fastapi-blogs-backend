from fastapi import APIRouter, HTTPException
from app.schemas.article import Article, ArticleCreate
from app.services.article_service import create_article
from app.deps import SessionDep

router = APIRouter()

@router.post("/", response_model=Article)
def create_new_article(article: ArticleCreate, db: SessionDep):
    existing_article = db.query(Article).filter(Article.title == article.title).first()
    if existing_article:
        raise HTTPException(status_code=400, detail="Article with this title already exists")

    db_article = create_article(db, article)
    return db_article
