"""
src/domain/models/economic_event.py
This file defines the EconomicEventModel model used for economic events.
"""

from typing import Optional, TypedDict


class EconomicCalendarEventModel(TypedDict):
    """
    Typed dictionary model representing an economic calendar event.

    Attributes:
        id (str): Unique identifier for the event.
        date (str): Date of the event (format 'dd/mm/yyyy').
        time (str): Time of the event (e.g., 'All Day' if the event lasts the entire day).
        zone (str): Geographic zone or region associated with the event.
        currency (Optional[str]): Currency related to the event, if applicable.
        importance (Optional[str]): Importance level of the event (e.g., 'low', 'medium', 'high').
        event (str): Description or name of the event.
        actual (Optional[str]): Reported actual value for the event, if available.
        forecast (Optional[str]): Forecasted value for the event, if available.
        previous (Optional[str]): Previously recorded value for the event, if available.
    """

    id: str
    date: str
    time: str
    zone: str
    currency: Optional[str]
    importance: Optional[str]
    event: str
    actual: Optional[str]
    forecast: Optional[str]
    previous: Optional[str]
