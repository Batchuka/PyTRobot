# test/test_celery_strategy.py

import sys
import unittest
from pathlib import Path
from contextlib import contextmanager

@contextmanager
def temporarily_add_to_path(path):
    """Adiciona um caminho ao sys.path temporariamente."""
    sys.path.insert(0, path)
    try:
        yield
    finally:
        sys.path.pop(0)

class TestStateCeleryTogether(unittest.TestCase):
    
    def setUp(self):
        # Inicializa o PyTRobot no diretório do projeto `new_project`
        project_dir    = Path(__file__).resolve().parent.parent / "pytrobot" / "scaffold" / "celery" / "project" 
        src_path       = Path(__file__).resolve().parent.parent / "pytrobot" / "scaffold" / "celery" / "project" / "pizza_bot_v2" 
        self.project_dir    = str(project_dir)
        self.src_path       = str(src_path)
        pass

    def test_application_initialization_and_start(self):

        with temporarily_add_to_path(self.project_dir):
            # Agora você pode importar o PyTRobot corretamente
            from pytrobot import PyTRobot

            pytrobot = PyTRobot(directory=str(self.src_path))

            # Verifica se as estratégias foram inicializadas automaticamente
            self.assertIsNotNone(pytrobot.strategies, "Estratégias não foram inicializadas.")
            
            # Verifica se pelo menos uma estratégia foi carregada
            self.assertGreater(len(pytrobot.strategies), 0, "Nenhuma estratégia foi carregada.")
            
            pytrobot.initialize_application()

            # Inicia a aplicação e verifica se há threads ativas
            pytrobot.start_application()

if __name__ == "__main__":
    unittest.main()