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

    def mt4_credentials(self) -> dict:
        """
        Get the MetaTrader 4 (MT4) account credentials.

        Returns:
            dict: A dictionary containing 'account', 'server', and 'password' and mt4_path.

        Raises:
            ValueError: If any of the required MT4 environment variables are not set.
        """
        account = os.getenv("ACCOUNT_MT4")
        server = os.getenv("SERVER_MT4")
        password = os.getenv("PASSWORD_MT4")
        mt4_path = os.getenv("MT4_PATHs")

        if not account or not server or not password or not mt4_path:
            raise ValueError("One or more MT4 credentials are not set")

        return {
            "account": account,
            "server": server,
            "password": password,
            "mt4_path": mt4_path
        }
