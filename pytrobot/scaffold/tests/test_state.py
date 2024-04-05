import unittest
from pytrobot.core.dataset_layer import TransactionData
from wmt_registro_di_bot.src.tools.chrome_tool import ChromeTool
from wmt_registro_di_bot.src.tools.desktop_tool import DesktopTool
from pytrobot.scaffold.src.states import SampleState

# Classe de teste unitário
class TestSampleState(unittest.TestCase):

    def setUp(self):

        # Instanciando as ferramentas reais
        #self.chrome_tool = ChromeTool(debugger_address='localhost:9222')
        #self.desktop_tool = DesktopTool()

        # Criando o objeto VerificaDiState com mocks
        self.state = SampleState(None, None)

        # Substituímos get_tool para retornar nossas instâncias reais para teste.
        #self.state.get_tool = lambda tool_name: {'ChromeTool': self.chrome_tool,'DesktopTool': self.desktop_tool}.get(tool_name)

        # preparado com dados para ser utilizado pelo estado durante o teste.
        self.mock_tdata = TransactionData('td_process_list', ['id', 'data', 'status'])
        self.mock_tdata.add_row(id='TESTE1', data='some_data')
        self.mock_tdata.add_row(id='123', data='some_data')
        #self.state.get_tdata = lambda name: self.mock_tdata if name == 'td_process_list' else None

    
    def test_execute(self):
        self.state.on_entry()
        self.state.execute()

    def tearDown(self):
        pass

# Permite que os testes sejam executados quando o script é rodado diretamente
if __name__ == '__main__':
    unittest.main()