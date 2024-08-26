import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.models.article import Article
from app.schemas.article import ArticleCreate
from app.tests.utils import create_article_in_db


def test_create_article(client: TestClient, session: Session):
    article_data = {
        "title": "New Article",
        "content": "New Content",
        "meta_description": "A quick brown fox jumps over the lazy dog",
        "author_name": "Hashir Hassan"
    }

    response = client.post("/api/v1/articles/", json=article_data)
    assert response.status_code == 200

    data = response.json()
    # match fields of response with fields that were given
    assert data["title"] == article_data["title"]
    assert data["content"] == article_data["content"]
    assert data["meta_description"] == article_data["meta_description"]
    assert data["author_name"] == article_data["author_name"]
    assert "id" in data

    # Verify the article was added to the database
    db_article = session.get(Article, data["id"])
    assert db_article is not None
    assert db_article.title == article_data["title"]
    assert db_article.content == article_data["content"]


def test_list_articles(client: TestClient, session: Session):
    # Create two articles
    create_article_in_db(session, ArticleCreate(title="Article for Ta-da Coinbase", content="A quick brown fox...", author_name="Hashir Hassan"))
    create_article_in_db(session, ArticleCreate(title="Article 2 for Ta-da Binance", content="Lorem Ipsum", meta_description="I am writing this to improve SEO"))

    response = client.get("/api/v1/articles/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["title"] == "Article for Ta-da Coinbase"
    assert data[1]["title"] == "Article 2 for Ta-da Binance"

def test_delete_article(client: TestClient, session: Session):
    article = create_article_in_db(session, ArticleCreate(title="For delete: Ta-da blog", content="A quick brown fox..."))
 
    response = client.delete(f"/api/v1/articles/{article.id}/")
    assert response.status_code == 204
    response = client.get("/api/v1/articles/")
    assert len(response.json()) == 0

