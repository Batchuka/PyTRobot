import unittest
from scaffold.objects.actions.action_sample import SampleAction

class TestSampleTool(unittest.TestCase):
    def test_use(self):
        acao = SampleAction()
        result = acao.perform()
        self.assertEqual(result, "Usado com sucesso")

    # Adicione mais métodos de teste conforme necessário

if __name__ == '__main__':
    unittest.main()