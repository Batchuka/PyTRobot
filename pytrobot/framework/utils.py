import logging
import os


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


def delete_all_temp_files():
    """
    Exclui todos os arquivos no diretório temporário, exceto 'placeholder.txt'.
    """

    temp_directory = '/home/seluser/temp'

    # Verifica se o diretório temporário existe
    if os.path.exists(temp_directory) and os.path.isdir(temp_directory):
        # Obtém a lista de arquivos no diretório temporário
        files = os.listdir(temp_directory)

        for file in files:
            # Verifica se o arquivo é diferente de 'placeholder.txt'
            if file != 'placeholder.txt':
                file_path = os.path.join(temp_directory, file)
                # Verifica se o caminho é um arquivo
                if os.path.isfile(file_path):
                    # Exclui o arquivo
                    os.remove(file_path)
                    #Logger.log(f"Deleted file: {file_path}")
                    print(f"Deleted file: {file_path}")
    else:
        # Logger.log(f"Temporary directory '{temp_directory}' not found")
        print(f"Temporary directory '{temp_directory}' not found")