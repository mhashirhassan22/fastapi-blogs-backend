from sqlalchemy.ext.declarative import declarative_base

# Base class for all models to inherit from
Base = declarative_base()

from app.db.models.article import Article
