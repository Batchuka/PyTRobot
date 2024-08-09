# pytrobot/core/decortador/log.py
from pytrobot.core.feature.config import ConfigManager
from pytrobot.core.feature.logging import Logger

def log_function_call(func):
    """
    Decorator that logs the name of the function whenever it is called.
    """

    def wrapper(*args, **kwargs):
        logger = Logger()
        logger.debug(f"Calling function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper