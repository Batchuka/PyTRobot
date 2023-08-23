from typing import Any
"""
"""


class Robot:
    """
    Essa classe implementa a estrutura do estado. Ela controla e separa as lógicas 
    e os diversos estados do robô. O controle desses estados é baseado no retorno 'robot.status()'. 
    """

    def __init__(self):
        self._status = False
        self._current_state = None
        self._next_state = None

    def __repr__(self) -> str:
        return f'Robot.{self._current_state}'

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if isinstance(value, bool):
            self._status = value
        else:
            raise ValueError(
                "The status value must be a Boolean (True or False).")

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, value):
        from .state import State
        if isinstance(value, State):
            self._current_state = value
        else:
            raise ValueError(
                "The current_state value must be a member of the State enumeration.")

    @property
    def next_state(self):
        return self._next_state

    @next_state.setter
    def next_state(self, value):
        from .state import State
        if isinstance(value, State):
            self._next_state = value
        else:
            raise ValueError(
                "The next_state value must be a member of the State enumeration.")

    def execute(self):
        """
        Executa a lógica principal do estado atual do robô. Deve ser implementado em cada subclasse.

        :return: Retorna o estado do robô após a execução da lógica.
        """
        pass

    def on_error(self):
        """
        Método invocado quando a execução do estado atual retorna 'False', indicando um erro.
        Deve implementar as tratativas de erro adequadas.

        :return: Retorna o próximo estado planejado após o tratamento de erro.
        """
        pass

    def on_exit(self):
        """
        Método invocado quando a execução do estado atual retorna 'True', indicando sucesso.
        Pode implementar ações de limpeza ou transição para o próximo estado.

        :return: Retorna o próximo estado planejado após a conclusão com sucesso.
        """
        pass

    def on_entry(self):
        """
        Primeiro método invocado ao entrar em qualquer estado. Pode ser usado para inicializações e acessos ao config.

        :return: Retorna o estado do robô após a inicialização.
        """
        pass
