# pytrobot/__init__.py

# API para o desenvolvedor implementar
from pytrobot.core import PyTRobot, State, First, BaseState, TransactionData, TransactionItem
from pytrobot.debug import debug_entrypoint as debug
from pytrobot.tasks import auto_import_states

# Definição dos elementos da API que serão publicamente acessíveis ao importar 'pytrobot'
__all__ = ['PyTRobot', 'State', 'First', 'BaseState', 'TransactionData', 'TransactionItem', 'debug', 'auto_import_states']

# Versão do pacote
__version__ = '3.1.0'