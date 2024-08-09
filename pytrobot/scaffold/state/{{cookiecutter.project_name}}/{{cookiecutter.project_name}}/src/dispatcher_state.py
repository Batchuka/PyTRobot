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

        print('Dados carregados com sucesso em TransactionData.')

    def on_exit(self):

        pass

    def on_error(self, error):

        pass
