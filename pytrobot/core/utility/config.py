# pytrobot/core/utility/config.py

from pytrobot.core.feature.config import ConfigManager

class ConfigKeyError(Exception):
    """Custom exception raised when a configuration key is missing or has a None value."""
    pass

def Value(config_key, default=None):
    """
    Returns the value of a configuration from the ConfigManager.
    If the value is None, raises a ConfigKeyError.
    """
    config_manager = ConfigManager()  # Obtém a instância singleton do ConfigManager
    value = config_manager.get_config(config_key, default)

    if value is None:
        raise ConfigKeyError(f"Configuration key '{config_key}' returned None. Please provide a valid value.")

    return value