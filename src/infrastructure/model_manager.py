"""
src/infrastructure/model_manager.py
this file contains the model manager ai
"""

from typing import List

from openai import OpenAI

from config.settings import Settings
from domain.models.chat_message import ChatMessageModel


class ModelManager:
    """
    Model manager for the ai
    """

    def __init__(self):
        settings = Settings()
        self.openai_key = settings.api_openai_key()
        self.model_name = "chatgpt-4o-latest"
        self.client = OpenAI(
            api_key=self.openai_key,
        )

    def generate_response(self, messages: List[ChatMessageModel]) -> str | None:
        """
        Generate a response from the AI.

        Args:
            messages (List[ChatMessageModel]): The list of chat messages to generate a response from.

        Returns:
            (str | None): The generated response from the AI.
        """

        response = self.client.chat.completions.create(
            model=self.model_name, messages=messages
        )
        return response.choices[0].message.content
