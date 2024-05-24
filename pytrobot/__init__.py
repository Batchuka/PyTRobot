# pytrobot/__init__.py

# API para o desenvolvedor implementar
from pytrobot.core import State, First, Thread   # Decoradores
from pytrobot.core import PyTRobot, BaseState, TransactionData, TransactionItem   # Classes
from pytrobot.tasks import auto_import_states

# Definição dos elementos da API que serão publicamente acessíveis ao importar 'pytrobot'
__all__ = ['State', 'First', 'Thread', 'PyTRobot', 'BaseState', 'TransactionData', 'TransactionItem', 'auto_import_states']