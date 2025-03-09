"""
src/config/headers.py
this file contains the headers for the requests
"""

import json
import random
from typing import Dict, List


class Headers:
    """
    Headers for the requests
    """

    def __init__(self):
        self.referers = [
            "https://www.google.com",
            "https://www.bing.com",
            "https://www.yahoo.com",
            "https://duckduckgo.com",
            "https://www.yandex.com",
            "https://www.baidu.com",
            "https://www.ecosia.org",
            "https://search.brave.com",
            "https://www.ask.com",
            "https://www.aol.com",
            "https://www.facebook.com",
            "https://twitter.com",
            "https://www.linkedin.com",
            "https://www.instagram.com",
            "https://www.youtube.com",
            "https://www.reddit.com",
            "https://www.pinterest.com",
            "https://www.tumblr.com",
            "https://www.quora.com",
            "https://www.microsoft.com",
            "https://www.apple.com",
            "https://www.amazon.com",
            "https://www.netflix.com",
            "https://www.paypal.com",
            "https://www.google.fr",
            "https://www.google.de",
            "https://www.google.es",
            "https://www.google.co.uk",
            "https://myaccount.google.com",
            "https://aboutme.google.com",
        ]

    def get_user_agents(self) -> List[str]:
        """
        Get the user agents for the requests.

        Returns:
            List[str]: A list of user agents.
        """
        with open("src/config/headers.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return data.get("user_agents", [])

    def get_headers(self) -> List[Dict[str, str]]:
        """
        Get the headers for the requests. This method generates
        a list of dictionaries, each containing the same base
        headers but with:
         - a different 'User-Agent'
         - a random 'Referer'

        Returns:
            List[Dict[str, str]]: A list of headers, each a dictionary
            containing User-Agent, Referer, and other default headers.
        """
        headers_list = []
        user_agents = self.get_user_agents()

        for user_agent in user_agents:
            random_referer = random.choice(self.referers)
            header_dict = {
                "User-Agent": user_agent,
                "Referer": random_referer,
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
            headers_list.append(header_dict)

        return headers_list
