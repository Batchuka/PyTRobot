from framework.config import Config
import logging
import os


def handle_exceptions(func):

    def wrapper(self, *args, **kwargs):
        try:
            func(self, *args, **kwargs)
            self.status = True
        except Exception as e:
            logging.error(
                f"Error in '{func.__name__}' of the {self.current_state}: {str(e)}")
            self.status = False

    return wrapper


def with_logging(func):

    def wrapper(self, *args, **kwargs):
        logging.debug(f"{self.current_state}.{func.__name__}")
        func(self, *args, **kwargs)
    return wrapper


def apply_decorator_to_all_methods(decorator):

    def class_decorator(cls):
        for name, value in vars(cls).items():
            if callable(value) and not name.startswith("__"):
                setattr(cls, name, decorator(value))
        return cls

    return class_decorator


def delete_all_temp_files():

    temp_directory = 'temp'

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
                    print(f"Deleted file: {file_path}")
    else:
        print(f"Temporary directory '{temp_directory}' not found")
