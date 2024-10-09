# pytrobot/core/strategy/celery/base_task.py

from celery import Task
from typing import Literal
from abc import ABC, abstractmethod
from pytrobot.core.utility.log import LogManager

class BaseTask(Task, ABC):
    # abstract = True
    def __init__(self):
        self.log_manager = LogManager()
        self.logger = LogManager().get_logger('SQS')

    def run(self, *args, **kwargs):
        # Chama o método de entrada antes de executar a lógica principal
        self.__on_entry()
        self.execute(*args, **kwargs)

    def __on_entry(self):
        """
        Método privado que chama o método on_entry do usuário.
        Pode incluir lógica adicional de inicialização, se necessário.
        """
        self.on_entry()

    @abstractmethod
    def on_entry(self):
        """
        Método abstrato de preparação para a execução da tarefa.
        Deve ser implementado pelo usuário para inicializar qualquer
        estado ou recurso necessário antes da execução da tarefa.
        """
        pass
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Define a lógica principal da tarefa.
        Deve ser implementado pelo usuário.
        """
        raise NotImplementedError("O método 'execute' deve ser implementado pelo worker.")