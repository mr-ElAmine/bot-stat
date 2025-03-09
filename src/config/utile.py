"""
src/config/utils.py
this file contains utilities functions that are used in the application.
"""

from time import sleep


def retry_on_failure(max_attempts=3, delay=5):
    """
    Decorator that retries executing the function if the result is None.

    Parameters:
        max_attempts (int): The maximum number of attempts before giving up.
        delay (int): The delay in seconds between each attempt.

    Returns:
        function: A decorator that wraps the target function with retry logic.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                result = func(*args, **kwargs)
                if result is not None:
                    return result
                print(f"Attempt {attempt} failed, retrying in {delay} seconds...")
                sleep(delay)
            return None

        return wrapper

    return decorator
