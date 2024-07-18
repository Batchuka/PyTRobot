import unittest
from pytrobot.core.strategies.state.dataset_layer import TransactionData
from {{cookiecutter.project_name}}.{{cookiecutter.project_name}}.src.sample_state import SampleState  # type:ignore

# Classe de teste unitário


class TestSampleState(unittest.TestCase):

    def setUp(self):

        # Criando o objeto SampleState com mocks
        self.state = SampleState(None)  # type:ignore

    def test_execute(self):
        self.state.on_entry()
        self.state.execute()

    def tearDown(self):
        pass


# Permite que os testes sejam executados quando o script é rodado diretamente
if __name__ == '__main__':
    unittest.main()
