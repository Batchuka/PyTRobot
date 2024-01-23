import unittest
from scaffold.objects.tools.tool_sample import SampleTool

class TestSampleTool(unittest.TestCase):
    def test_use(self):
        ferramenta = SampleTool()
        result = ferramenta.use()
        self.assertEqual(result, "Usado com sucesso")

    # Adicione mais métodos de teste conforme necessário

if __name__ == '__main__':
    unittest.main()