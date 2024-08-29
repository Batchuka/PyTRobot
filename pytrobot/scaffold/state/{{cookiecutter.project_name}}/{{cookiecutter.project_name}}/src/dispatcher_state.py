from pytrobot import State, First, BaseState, TransactionData
import time


@First
@State('PerformerState', '_FinisherState')
class DispatcherState(BaseState):
    """
    Um estado inicial de exemplo que pode ser usado como ponto de partida.
    Este estado simula a carga de dados em TransactionData e gerencia exceções.
    """

    def on_entry(self):

        print('Preparando para obter dados de transação...')
        TransactionData(['id', 'data'])

    def execute(self):

        transaction_data = TransactionData()

        for i in range(5):
            transaction_data.add_item(id=i, data=f'Sample Data {i}')
            time.sleep(2)
        
        self.valor_negocio = 'algo que depende da lógica' # Três valores possíveis

        print('Dados carregados com sucesso em TransactionData.')

    def on_exit(self):

        if self.valor_negocio == 'isso': self.transition('FazerIssoState')
        elif self.valor_negocio == 'aquilo' : self.transition('FazerAquiloState')
        elif self.valor_negocio == 'etc' : self.transition('FazerEtcState')
        else : self.transition('_FinisherState')

    def on_error(self, error):

        print(error)
        self.transition('_FinisherState')
