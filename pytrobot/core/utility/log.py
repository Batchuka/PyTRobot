# pytrobot/core/utility/log.py
import logging
from typing import Literal
from pytrobot.core.feature.logging import Logger


# Function to Log in to the Framework standard
def Log(message: str, level: Literal['INFO', 'DEBUG', 'ERROR', 'WARN'] = 'INFO'):
    """
    Send message to the output in the Logger pattern
    """
    logger = Logger()
    if level == 'DEBUG':
        logger.debug(message)
    elif level == 'ERROR':
        logger.error(message)
    elif level == 'WARN':
        logger.log(message, level=logging.WARNING)
    else:
        logger.info(message)