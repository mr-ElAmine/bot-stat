"""
src/infrastructure/broker_mt4.py
This module defines the Broker class, which interacts with MetaTrader 4 (MT4) to execute trades.
"""

from typing import Optional

import MetaTrader5 as mt5

from src.config.settings import Settings


class Broker:
    """
    A broker interface for MetaTrader 4 (MT4), allowing automated trading based on technical indicators.
    """

    def __init__(
        self,
        account: Optional[int] = None,
        password: Optional[str] = None,
        server: Optional[str] = None,
    ):
        """
        Initializes the connection to MT4.

        Args:
            account (int, optional): MT4 account number.
            password (str, optional): MT4 account password.
            server (str, optional): MT4 broker server name.
        """
        if account is None or password is None or server is None:
            settings = Settings()
            credentials = settings.mt4_credentials()
            account = credentials["account"]
            password = credentials["password"]
            server = credentials["server"]

        if not mt5.initialize():
            raise ConnectionError("MT4 initialization failed")

        authorized = mt5.login(int(account), password=password, server=server)
        if not authorized:
            raise ConnectionError(f"MT4 login failed: {mt5.last_error()}")

        print(f"Connected to MT4 account {account} on {server}")
