# pytrobot/core/utility/log.py
import logging
import inspect
from typing import Literal
from pytrobot.core.singleton import Singleton

class LogManager(metaclass=Singleton):
    def __init__(self):
        self._configure_loggers()

    def _configure_loggers(self):
        # Logger para State
        self.state_logger = logging.getLogger('State')
        state_handler = logging.StreamHandler()
        state_formatter = logging.Formatter('[STATE] %(asctime)s - %(levelname)s - %(message)s')
        state_handler.setFormatter(state_formatter)
        self.state_logger.addHandler(state_handler)
        self.state_logger.setLevel(logging.INFO)

        # Logger para Queue
        self.queue_logger = logging.getLogger('Queue')
        queue_handler = logging.StreamHandler()
        queue_formatter = logging.Formatter('[QUEUE] %(asctime)s - %(levelname)s - %(message)s')
        queue_handler.setFormatter(queue_formatter)
        self.queue_logger.addHandler(queue_handler)
        self.queue_logger.setLevel(logging.INFO)

        # Redireciona logs do Queue para o logger customizado
        logging.getLogger('queue').addHandler(queue_handler)

    def get_logger(self, name: Literal['State', 'Queue']):
        """Obtém o logger correto para 'State' ou 'Queue'."""
        if name == 'State':
            return self.state_logger
        elif name == 'Queue':
            return self.queue_logger
        else:
            raise ValueError("Logger name must be 'State' or 'Queue'")

    def log(self, logger, message: str, level: Literal['INFO', 'DEBUG', 'ERROR', 'WARN'] = 'INFO'):
        """
        Loga a mensagem usando o logger apropriado, incluindo contexto de classe e método.
        """
        # Obtém o frame chamador para extrair o contexto de classe e método
        frame = inspect.currentframe()
        
        # Verifica se o frame e o frame.f_back não são None antes de acessar atributos
        if frame is not None and frame.f_back is not None:
            caller_frame = frame.f_back.f_back if frame.f_back and frame.f_back.f_back else frame.f_back
            if 'self' in caller_frame.f_locals:
                class_name = caller_frame.f_locals['self'].__class__.__name__
                method_name = caller_frame.f_code.co_name
                # Cria a mensagem de log com classe e método
                formatted_message = f"[{class_name}.{method_name}] {message}"
            else:
                # Caso não consiga obter o contexto, usa a mensagem original
                formatted_message = message
        else:
            formatted_message = message
            
        # Usa o nível de log apropriado
        if level == 'DEBUG':
            logger.debug(formatted_message)
        elif level == 'ERROR':
            logger.error(formatted_message)
        elif level == 'WARN':
            logger.warning(formatted_message)
        else:
            logger.info(formatted_message)
