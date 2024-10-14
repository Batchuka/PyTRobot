import logging
import inspect
from pytrobot.core.singleton import Singleton

class LogManager(metaclass=Singleton):
    def __init__(self):
        self._configure_loggers()

    def _configure_loggers(self):
        """
        Configura os loggers para 'State' e 'SQS' com formatos personalizados.
        """
        self.loggers = {
            'PyTRobot': self._create_logger('PyTRobot'),
            'State': self._create_logger('State'),
            'SQS': self._create_logger('SQS')
        }

    def _create_logger(self, name: str) -> logging.Logger:
        """
        Cria um logger que utiliza um formato dinâmico com o contexto (classe e método) capturado na execução.
        O formato do log será: [name] [Classe.Metodo] %(asctime)s - %(levelname)s - %(message)s.
        """
        logger = logging.getLogger(name)
        handler = logging.StreamHandler()

        # Define um Formatter personalizado para que o contexto seja injetado dinamicamente
        class ContextFormatter(logging.Formatter):
            def format(self, record):
                # Captura o contexto automaticamente
                frame = inspect.currentframe()

                # Itera sobre os frames para encontrar o correto
                depth = 0
                while frame and depth < 10:  # Ajuste a profundidade se necessário
                    if frame.f_code.co_name != 'emit':  # Pulando a função 'emit' que não nos interessa
                        caller_frame = frame
                    frame = frame.f_back
                    depth += 1

                # Adiciona o contexto dinâmico ao record
                if caller_frame and 'self' in caller_frame.f_locals:
                    class_name = caller_frame.f_locals['self'].__class__.__name__
                    method_name = caller_frame.f_code.co_name
                    context = record.__dict__['context'] = f"[{class_name}.{method_name}]"
                else:
                    context = record.__dict__['context'] = "[UnknownContext]"

                # Formato do log com a ordem que você pediu
                formatted_time = self.formatTime(record)  # Formata o tempo
                formatted_level = f"|{record.levelname:<8}"  # Nível de log (alinhado à esquerda)
                formatted_name = f" |{record.name:<10}"  # Nome do logger com preenchimento à esquerda (tamanho 10)
                formatted_context = f"{context} —"  # Contexto com preenchimento à esquerda (tamanho 20)
                formatted_message = f"{record.getMessage()}"  # A mensagem original

                # Formato do log
                return f"{formatted_time} {formatted_level} {formatted_name} {formatted_context} {formatted_message}"

        # Define o formato básico do log (sem o contexto)
        formatter = ContextFormatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def get_logger(self, name: str) -> logging.Logger:
        """
        Obtém o logger correto para 'State' ou 'SQS'.
        """
        if name in self.loggers:
            return self.loggers[name]
        raise ValueError("Logger name must be 'State' ou 'SQS'")