"""
src/main.py
this file contains the main bot
"""

from infrastructure.broker_manager import BrokerManager

broker = BrokerManager()
market_data = broker.get_market_data()
print(market_data)
