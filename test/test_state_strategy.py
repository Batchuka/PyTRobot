# test/test_new_project_state.py

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

class TestNewProjectState(unittest.TestCase):
    
    def setUp(self):
        # Inicializa o PyTRobot no diretório do projeto `new_project`
        project_dir    = Path(__file__).resolve().parent.parent / "pytrobot" / "scaffold" / "state" / "new_project" 
        src_path       = Path(__file__).resolve().parent.parent / "pytrobot" / "scaffold" / "state" / "new_project" / "new_project" 
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

            # Inicia a aplicação e verifica se há threads ativas
            pytrobot.start_application()
            active_threads = pytrobot.multithread_manager.get_number_active_threads()
            self.assertGreater(active_threads, 0, "Nenhuma thread ativa após iniciar a aplicação.")

if __name__ == "__main__":
    unittest.main()