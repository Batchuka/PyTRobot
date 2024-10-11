# pytrobot\core\decortador\config.py
from functools import wraps

from pytrobot.core.feature.config import ConfigManager

def Config(config_key, default=None):
    """
    Decorador para injetar um valor de configuração na função decorada.

    :param config_key: Chave da configuração a ser injetada.
    :param default: Valor padrão a ser usado se a configuração não for encontrada.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Obtém o valor da configuração usando o ConfigManager
            config_manager = ConfigManager()  # Obtém a instância singleton do ConfigManager
            config_value = config_manager.get_config(config_key, default)
            
            # Injeta o valor da configuração nos argumentos da função
            return func(config_value, *args, **kwargs)
        
        return wrapper
    return decorator
