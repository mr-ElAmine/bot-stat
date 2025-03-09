"""
src/main.py
this file contains the main bot
"""

from infrastructure.database_manager import Base, DatabaseManager
from infrastructure.model_manager import ModelManager
from infrastructure.news_and_calendar_manager import NewsAndCalendarManager

db_manager = DatabaseManager()
Base.metadata.create_all(db_manager.engine)

news_and_calendar_manager = NewsAndCalendarManager()
model_manager = ModelManager()

context_news_and_economic_calendar = (
    news_and_calendar_manager.get_context_news_and_economic_calendar()
)

rp = model_manager.generate_response(context_news_and_economic_calendar)
print(rp)
