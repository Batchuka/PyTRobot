import unittest
from pytrobot.core.dataset_layer import TransactionData
# from {{cookiecutter.project_name}}_bot.{{cookiecutter.project_name}}.src.sample_state import SampleState ← importar seu estado

# Classe de teste unitário
class TestSampleState(unittest.TestCase):

    def setUp(self):
        pass

        # prepare o mock para as funções que são chamadas internamente a sua classe

        # # Criando o objeto SampleState com mocks
        # self.state = SampleState(None) ← isntanciar seu estado

    
    def test_execute(self):
        self.state.on_entry()
        self.state.execute()

    def tearDown(self):
        pass

# Permite que os testes sejam executados quando o script é rodado diretamente
if __name__ == '__main__':
    unittest.main()