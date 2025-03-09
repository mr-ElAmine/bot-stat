"""
src/infrastructure/technical_indicator_manager.py
This module provides a class for enriching a stock market DataFrame with technical indicators.
"""

from pandas import DataFrame
from ta import (
    add_all_ta_features,
    add_momentum_ta,
    add_others_ta,
    add_trend_ta,
    add_volatility_ta,
    add_volume_ta,
)


class TechnicalIndicatorManager:
    """
    This class enriches a stock market DataFrame with various technical indicators.
    It requires a DataFrame containing at least the columns 'Open', 'High', 'Low',
    'Close', and 'Volume' to compute the indicators.
    """

    def __init__(self, data: DataFrame):
        """
        Initializes the TechnicalIndicatorManager with stock market data.

        Args:
            data (DataFrame): A DataFrame containing stock market data with required columns.
        """
        self.data = data.copy()

    def add_all_ta_features(self) -> DataFrame:
        """
        Adds all available technical indicators to the DataFrame.

        Returns:
            DataFrame: The DataFrame enriched with all technical indicators provided by `ta`.
        """
        data = self.data.copy()
        return add_all_ta_features(
            data,
            open="Open",
            high="High",
            low="Low",
            close="Close",
            volume="Volume",
            fillna=True,
        )

    def add_momentum_ta(self) -> DataFrame:
        """
        Adds momentum indicators to the DataFrame.

        Momentum indicators help identify the speed and strength of price movements.

        Returns:
            DataFrame: The DataFrame enriched with momentum indicators.
        """
        data = self.data.copy()
        return add_momentum_ta(
            data, high="High", low="Low", close="Close", volume="Volume", fillna=True
        )

    def add_others_ta(self) -> DataFrame:
        """
        Adds miscellaneous technical indicators to the DataFrame.

        These indicators include statistics such as daily returns and logarithmic returns.

        Returns:
            DataFrame: The DataFrame enriched with miscellaneous technical indicators.
        """
        data = self.data.copy()
        return add_others_ta(data, close="Close", fillna=True)

    def add_trend_ta(self) -> DataFrame:
        """
        Adds trend indicators to the DataFrame.

        Trend indicators help determine the direction of the market movement.

        Returns:
            DataFrame: The DataFrame enriched with trend indicators.
        """
        data = self.data.copy()
        return add_trend_ta(data, high="High", low="Low", close="Close")

    def add_volatility_ta(self) -> DataFrame:
        """
        Adds volatility indicators to the DataFrame.

        Volatility indicators measure price fluctuations over a given period.

        Returns:
            DataFrame: The DataFrame enriched with volatility indicators.
        """
        data = self.data.copy()
        return add_volatility_ta(
            data, high="High", low="Low", close="Close", fillna=True
        )

    def add_volume_ta(self) -> DataFrame:
        """
        Adds volume indicators to the DataFrame.

        Volume indicators analyse trading volume to provide insights into market activity.

        Returns:
            DataFrame: The DataFrame enriched with volume indicators.
        """
        data = self.data.copy()
        return add_volume_ta(
            data, high="High", low="Low", close="Close", volume="Volume", fillna=True
        )
