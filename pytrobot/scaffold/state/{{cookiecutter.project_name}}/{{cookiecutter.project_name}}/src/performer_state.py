from pytrobot import State, BaseState, TransactionData

@State('_FinisherState', '_FinisherState')
class PerformerState(BaseState):
    """
    Um estado inicial de exemplo que pode ser usado como ponto de partida.
    Este estado simula a carga de dados em TransactionData e gerencia exceções.
    """

    def on_entry(self):

        print('DispatcherState: Preparando para obter dados de transação...')
        self.td = TransactionData()

    def execute(self):

        if 2 < self.retry_counter < 4:
            print(
                f'DispatcherState: Simulando uma exceção. Tentativas restantes: {self.retry_counter}')
            self.retry_counter -= 1
            raise Exception("Erro simulado durante a execução")

        while self.td.transaction_item:
            print(self.td.transaction_item['data'])
            print(f'Done item : {self.td.transaction_number}')
            self.td.get_next_item()

    def on_exit(self):

        pass

    def on_error(self, error):

        pass
        print('Algo para tratar possíveis erros deve ser feito.')
