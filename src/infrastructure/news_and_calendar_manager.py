"""
src/infrastructure/news_and_calendar_manager.py
This file contains the news and calendar manager for investing.com.
"""

import random
from datetime import datetime, timedelta
from time import sleep
from typing import List, Optional

import investpy
import requests
from bs4 import BeautifulSoup

from config.headers import Headers
from config.utile import retry_on_failure
from domain.entity.article import ArticleEntity
from domain.models.article import ArticleModel
from domain.models.chat_message import ChatMessageModel
from domain.models.economic_calendar_event import EconomicCalendarEventModel
from infrastructure.database_manager import DatabaseManager


class NewsAndCalendarManager:
    """
    News and calendar manager for investing.com.
    """

    def __init__(self) -> None:
        """
        Initialize the news and calendar manager.
        """
        self.base_url = "https://www.investing.com/"
        self.news_path = "news/forex-news"
        self.headers = Headers().get_headers()
        self.session = requests.Session()
        self.database_manager = DatabaseManager()

    def get_article_from_db(self, link: str) -> Optional[ArticleModel]:
        """
        Checks if an article with the given link already exists in the database.

        Args:
            link (str): The article link.

        Returns:
            Optional[ArticleModel]: The existing instance or None if not found.
        """
        with self.database_manager.get_database_connection() as session:
            return (
                session.query(ArticleEntity).filter(ArticleEntity.link == link).first()
            )

    @retry_on_failure()
    def get_articles_from_page(self, page: int = 1) -> List[ArticleModel]:
        """
        Retrieve article titles, links, and content from a given news page.

        Args:
            page (int): The page number to fetch. Defaults to 1.

        Returns:
            List[ArticleModel]: A list containing [title, link, content] for each article found.
                                Returns an empty list if no articles are found or if an error occurs.
        """
        articles: List[ArticleModel] = []

        header = random.choice(self.headers)
        self.session.headers.update(header)

        try:
            self.session.get(self.base_url, timeout=10)
        except requests.RequestException as e:
            print(f"Error retrieving cookies: {e}")
            return articles

        url = f"{self.base_url}{self.news_path}"
        if page > 1:
            url = f"{url}/{page}"

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            news_list = soup.find("ul", {"data-test": "news-list"})
            if not news_list:
                print("No news found.")
                return articles

            for li in news_list.find_all("li"):
                a_tag = li.find("a", {"data-test": "article-title-link"})
                if not a_tag:
                    continue

                title = a_tag.get_text(strip=True)
                link = a_tag.get("href")
                if not link:
                    continue

                article = self.get_article_from_db(link)
                if not article:
                    content = self.get_article_content(link) or ""
                    article = ArticleEntity(title=title, link=link, content=content)
                    self.database_manager.create_to_database(article)

                    sleep(5)
                articles.append(article)

            return articles

        except requests.RequestException as e:
            print(f"Error fetching news: {e} {header}")
            return articles

    @retry_on_failure()
    def get_article_content(self, url: str) -> Optional[str]:
        """
        Fetch the full article text from a given URL.

        Args:
            url (str): The URL of the article.

        Returns:
            Optional[str]: The article text if successful, None otherwise.
        """
        header = random.choice(self.headers)
        self.session.headers.update(header)

        try:
            self.session.get(self.base_url, timeout=10)
        except requests.RequestException as e:
            print(f"Error retrieving cookies: {e}")
            return None

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            article_div = soup.find("div", id="article")
            if article_div is None:
                return None

            return article_div.get_text(strip=True)

        except requests.RequestException as e:
            print(f"Error fetching article: {e} {header}")
            return None

    def get_articles(self, nombre_page: int = 5) -> List[List[ArticleModel]]:
        """
        Retrieve articles from multiple pages.

        Args:
            nombre_page (int): The number of pages to fetch. Defaults to 5.

        Returns:
            List[List[ArticleModel]]: A list of pages, where each page is a list of [title, link, content].
        """
        all_articles: List[List[ArticleModel]] = []

        for page_number in range(1, nombre_page + 1):
            page_articles = self.get_articles_from_page(page_number)
            all_articles.append(page_articles)

        return all_articles

    @retry_on_failure()
    def get_calendar_events(
        self, from_date: datetime, to_date: datetime
    ) -> List[EconomicCalendarEventModel]:
        """
        Get economic calendar events.

        Args:
            from_date (datetime): The start date of the economic calendar events.
            to_date (datetime): The end date of the economic calendar events.

        Returns:
            List[EconomicCalendarEventModel]: The list of economic calendar events.
        """
        df = investpy.news.economic_calendar(
            from_date=from_date.strftime("%d/%m/%Y"),
            to_date=to_date.strftime("%d/%m/%Y"),
        )
        return df.to_dict(orient="index")

    def get_context_news_and_economic_calendar(self) -> List[ChatMessageModel]:
        """
        Retrieves recent news articles and economic calendar events within a time range,
        then formats them as chat messages with a unified system instruction.

        Returns:
            List[ChatMessageModel]: A list of chat messages containing news and calendar data.
        """
        from_date = datetime.today()
        to_date = datetime.today() + timedelta(days=5)

        economic_calendar = self.get_calendar_events(
            from_date=from_date, to_date=to_date
        )
        articles = self.get_articles_from_page(3)

        messages: List[ChatMessageModel] = []

        if economic_calendar:
            messages.append(
                {
                    "role": "user",
                    "content": f"Economic Calendar Events from {from_date.date()} to {to_date.date()}: {economic_calendar}",
                }
            )

        news_message = "Latest news articles:\n" + "\n".join(
            f"- {article.title}: {article.content}" for article in articles
        )
        messages.append({"role": "user", "content": news_message})

        return messages
