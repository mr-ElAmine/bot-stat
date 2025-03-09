"""
src/infrastructure/broker_mt4.py
This module defines the Manager class, which interacts with MetaTrader 4 (MT4) to execute trades.
"""

from typing import Optional

import MetaTrader5 as mt5
from pandas import DataFrame, to_datetime

from config.settings import Settings


class BrokerManager:
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

    def shutdown(self) -> None:
        """
        Properly closes the connection to MT4.
        """
        mt5.shutdown()
        print("Disconnected from MT4.")

    def get_market_data(
        self,
        symbol: str = "EURUSD",
        timeframe: int = mt5.TIMEFRAME_M1,
        num_bars: int = 100,
    ) -> DataFrame:
        """
        Retrieves historical market data from MetaTrader 4 and returns it as a pandas DataFrame.

        Args:
            symbol (str, optional): The financial instrument (e.g., "EURUSD") (default: EURUSD).
            timeframe (int, optional): The timeframe for data retrieval (default: M1 - 1 Minute).
            num_bars (int, optional): The number of historical bars to retrieve (default: 100).

        Returns:
            DataFrame: A DataFrame containing the historical market data with columns:
                       ['time', 'open', 'high', 'low', 'close', 'tick_volume', 'spread', 'real_volume'].

        Raises:
            ValueError: If no data is retrieved or an issue occurs with the MT4 connection.
        """
        if not mt5.initialize():
            raise ConnectionError("Failed to initialize connection with MetaTrader 5.")

        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_bars)

        if rates is None or len(rates) == 0:
            mt5.shutdown()
            raise ValueError(
                f"No data retrieved for {symbol}. Check the symbol and connection."
            )

        df = DataFrame(rates)

        df["time"] = to_datetime(df["time"], unit="s")

        mt5.shutdown()

        return df
