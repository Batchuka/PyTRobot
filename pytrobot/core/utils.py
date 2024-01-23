import logging

def HandleException(func):
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


def WithLog(func):
    """
    Um decorator que registra a chamada de uma função com informações de depuração.

    :param func: A função a ser decorada.
    """

    def wrapper(self, *args, **kwargs):
        # Logger.log(f"{self.current_state}.{func.__name__}", logging.DEBUG)
        print(f"{self.current_state}.{func.__name__}", logging.DEBUG)
        func(self, *args, **kwargs)
    return wrapper


def ApplyToMethods(decorator):
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


def print_pytrobot_banner():
    """Exibe o banner do pytrobot."""
    banner_lines = [
        "  _____        _______          _",
        " |  __ \__   _|__   __|        | |     o   _",
        " | |__) \ \ / /  | |_ ___  ___ | |__  _|_ | |__",
        " |  ___/ \ V /   | | V __|/ _ \|  _ \/   \|  __|",
        " | |      | |    | |  /  | |_| | |_)( * * ) |",
        " |_|      |_|    |_|__|   \___/|____/\---/|_|",
        " ____________________________________________",
        "|____________________________________________|",
        "  -- Transactional State Robot for Python --",
        "               Copyright © 2023",
        "\n\n"
    ]
    print("\n".join(banner_lines))


def pytrobot_print(*args, **kwargs):
    """Função print personalizada para redirecionar para o logger."""
    message = " ".join(map(str, args))
    Logger.log(message, level=kwargs.get('level', logging.INFO))


class Logger:
    """Um logger personalizado para o pytrobot."""
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._setup_logger()
        return cls._instance

    @staticmethod
    def _setup_logger():
        logger = logging.getLogger('pytrobot')
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s  %(levelname)s  %(message)s", datefmt="%d-%m-%Y %H:%M:%S")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def log(message, level=logging.INFO):
        logger = Logger.get_instance()
        logger.log(level, message)