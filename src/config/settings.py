"""
src/config/settings.py
This file contains the settings for the bot.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Settings for the bot, including API keys and MT4 account credentials.
    """

    def api_openai_key(self) -> str:
        """
        Get the API key for OpenAI.

        Returns:
            str: The API key.

        Raises:
            ValueError: If the API_KEY_OPENAI environment variable is not set.
        """
        openai_key = os.getenv("API_KEY_OPENAI")

        if openai_key is None:
            raise ValueError("API_KEY_OPENAI is not set")

        return openai_key
