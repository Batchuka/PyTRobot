import unittest
from unittest.mock import patch, MagicMock
from pytrobot.scaffold.src.states import SampleState

# Classe de teste unitário
class TestSampleState(unittest.TestCase):

    def setUp(self):
        
        # Objetos de acesso para um Estado
        self.mock_access_dataset_layer = MagicMock()
        self.mock_access_object_layer = MagicMock()

        # Criando o objeto VerificaDiState com mocks
        self.state = SampleState(self.mock_access_dataset_layer, self.mock_access_object_layer)
    
    def test_execute(self):
        self.state.execute()

    def tearDown(self):
        pass

# Permite que os testes sejam executados quando o script é rodado diretamente
if __name__ == '__main__':
    unittest.main()