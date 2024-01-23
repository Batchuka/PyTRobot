import unittest
from scaffold.objects.states.state_sample import SampleState

# Classe de teste unitário
class TestSampleState(unittest.TestCase):
    def test_execute(self):
        estado = SampleState()
        result = estado.execute()
        self.assertEqual(result, "Executado")

    # Adicione mais métodos de teste conforme necessário

# Permite que os testes sejam executados quando o script é rodado diretamente
if __name__ == '__main__':
    unittest.main()