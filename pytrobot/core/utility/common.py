# pytrobot\core\utility\common.py
import sys
import logging
from pathlib import Path
from contextlib import contextmanager
logger = logging.getLogger('PyTRobot')


# contextmanager para adicionar temporariamente ao sys.path
@contextmanager
def temporarily_add_to_path(path):
    """Adiciona um caminho ao sys.path temporariamente."""
    sys.path.insert(0, path)
    try:
        yield
    finally:
        sys.path.pop(0)

def add_to_path(path):
    """
    Adiciona o caminho ao sys.path.
    """
    resolved_path = str(Path(path).resolve())
    if resolved_path not in sys.path:
        sys.path.append(resolved_path)
        logger.info(f"Caminho adicionado ao sys.path: {resolved_path}")
    else:
        logger.warning(f"Caminho já está presente no sys.path: {resolved_path}")