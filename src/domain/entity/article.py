"""
src/domain/entity/article.py

This module defines the ArticleEntity, which represents an article in the database.
The entity includes a unique identifier (generated as a UUID), a title, a unique link, and the article content.
"""

import uuid

from sqlalchemy import Column, String, Text

from infrastructure.database_manager import Base


class ArticleEntity(Base):
    """
    Represents an article entity in the database.

    Attributes:
        id (str): Unique identifier for the article, generated as a UUID.
        title (str): Title of the article.
        link (str): Unique link to the article.
        content (str): Full content of the article.
    """

    __tablename__ = "articles"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    title = Column(Text, nullable=False)
    link = Column(Text, unique=True, nullable=False)
    content = Column(Text)
