"""
src/config/settings.py
This file contains the settings for the bot.
"""

import os


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

    def mt4_credentials(self) -> dict:
        """
        Get the MetaTrader 4 (MT4) account credentials.

        Returns:
            dict: A dictionary containing 'account', 'server', and 'password'.

        Raises:
            ValueError: If any of the required MT4 environment variables are not set.
        """
        account = os.getenv("MT4_ACCOUNT")
        server = os.getenv("MT4_SERVER")
        password = os.getenv("MT4_PASSWORD")

        if not account or not server or not password:
            raise ValueError("One or more MT4 credentials are not set")

        return {
            "account": account,
            "server": server,
            "password": password,
        }
