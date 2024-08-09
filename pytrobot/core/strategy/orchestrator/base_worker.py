# pytrobot/core/strategy/orchestrator/base_worker.py

from celery import Task
from abc import ABC, abstractmethod

class BaseWorker(Task, ABC):
    abstract = True

    def run(self, *args, **kwargs):
        # Chama o método de entrada antes de executar a lógica principal
        self._on_entry()
        self.execute(*args, **kwargs)

    @abstractmethod
    def on_entry(self):
        """
        Método abstrato de preparação para a execução da tarefa.
        Deve ser implementado pelo usuário para inicializar qualquer
        estado ou recurso necessário antes da execução da tarefa.
        """
        pass

    def _on_entry(self):
        """
        Método privado que chama o método on_entry do usuário.
        Pode incluir lógica adicional de inicialização, se necessário.
        """
        self.on_entry()

    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Define a lógica principal da tarefa.
        Deve ser implementado pelo usuário.
        """
        raise NotImplementedError("O método 'execute' deve ser implementado pelo worker.")