import logging

from pytrobot.core.transitions import TransitionRegistry


def State(cls):
    registry[cls.__name__] = cls
    return cls


def Tool(cls):
    registry[cls.__name__] = cls
    return cls


def Action(cls):
    registry[cls.__name__] = cls
    return cls


def handle_exceptions(func):
    """
    Um decorator que envolve a função fornecida com tratamento de exceções genéricas.
    Se a função for executada com sucesso, atualiza o status do robô para True. Se ocorrer
    uma exceção, registra um erro e atualiza o status do robô para False.

    :param func: A função a ser decorada.
    """

    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
            self.status = True
        except Exception as e:
            # Logger.log(
            #     f"Error in '{func.__name__}' of the {self.current_state}: {str(e)}", logging.ERROR)
            print(f"Error in '{func.__name__}' of the {self.current_state}: {str(e)}", logging.ERROR)
            self.status = False

    return wrapper


def with_logging(func):
    """
    Um decorator que registra a chamada de uma função com informações de depuração.

    :param func: A função a ser decorada.
    """

    def wrapper(self, *args, **kwargs):
        # Logger.log(f"{self.current_state}.{func.__name__}", logging.DEBUG)
        print(f"{self.current_state}.{func.__name__}", logging.DEBUG)
        func(self, *args, **kwargs)
    return wrapper


def apply_decorator_to_all_methods(decorator):
    """
    Um decorator de classe que aplica um decorator fornecido a todos os métodos da classe.

    :param decorator: O decorator a ser aplicado.
    """

    def class_decorator(cls):
        for name, value in vars(cls).items():
            if callable(value) and not name.startswith("__"):
                setattr(cls, name, decorator(value))
        return cls

    return class_decorator

