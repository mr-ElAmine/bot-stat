"""
src/domain/models/article.py
This module defines the ArticleModel, which represents the structure of a news article.
"""

from typing import TypedDict


class ArticleModel(TypedDict):
    """
    Represents a news article.

    Attributes:
        title (str): The title of the article.
        link (str): The URL linking to the full article.
        content (str): The main text content of the article.
    """

    title: str
    link: str
    content: str
