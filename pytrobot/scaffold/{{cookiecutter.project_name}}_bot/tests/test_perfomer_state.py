import unittest
from pytrobot.core.dataset_layer import TransactionData
from {{cookiecutter.project_name}}_bot.{{cookiecutter.project_name}}.src.performer_state import PerfomerState  # type:ignore

# Classe de teste unitário


class TestPerfomerState(unittest.TestCase):

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