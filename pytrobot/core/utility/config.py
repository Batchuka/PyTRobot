# pytrobot/core/utility/config.py

from pytrobot.core.feature.config import ConfigManager

# Function to get configuration values
def Value(config_key, default=None):
    """
    Returns the value of a configuration from the ConfigManager.
    """
    config_manager = ConfigManager()  # Obtém a instância singleton do ConfigManager
    return config_manager.get_config(config_key, default)
