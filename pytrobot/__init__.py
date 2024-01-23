# pytrobot/__init__.py

# API para o desenvolvedor implementar
from pytrobot.core import PyTRobot, State, Action, Tool, Transition
from pytrobot.core.states.base_state import BaseState
from pytrobot.core.actions.base_action import BaseAction
from pytrobot.core.tools.base_tool import BaseTool

# Definição dos elementos da API que serão publicamente acessíveis ao importar 'pytrobot'
__all__ = ['PyTRobot', 'Transition', 'State', 'Action', 'Tool', 'BaseState', 'BaseAction', 'BaseTool']

# Versão do pacote
__version__ = '3.0.0'