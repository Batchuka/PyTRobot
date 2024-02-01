# pytrobot/__init__.py

# API para o desenvolvedor implementar
from pytrobot.core import PyTRobot, State, Action, Tool, Transition, First
from pytrobot.core.states.base_state import BaseState
from pytrobot.core.actions.base_action import BaseAction
from pytrobot.core.tools.base_tool import BaseTool
from pytrobot.debug import debug_entrypoint as debug
from pytrobot.debug import auto_import_classes as auto_import

# Definição dos elementos da API que serão publicamente acessíveis ao importar 'pytrobot'
__all__ = ['PyTRobot', 'Transition', 'State', 'Action', 'Tool', 'First', 'BaseState', 'BaseAction', 'BaseTool', 'debug', 'auto_import']

# Versão do pacote
__version__ = '3.0.0'