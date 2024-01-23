from pytrobot import State, Transition, BaseState

@State
@Transition('SampleState', 'StateOnSucess', 'StateOnError')
class SampleState(BaseState):
    """
    Um estado inicial de exemplo que pode ser usado como ponto de partida.
    """

    def on_entry(self):
        # Este método é chamado quando a máquina de estados entra neste estado.
        print("Entrando no ExemploEstadoInicial.")

    def execute(self):
        # Este método contém a lógica principal a ser executada neste estado.
        print("Executando a lógica do ExemploEstadoInicial.")
        # Aqui você pode adicionar condições ou lógica para determinar o sucesso ou falha.
        # Por exemplo:
        # if alguma_condicao_de_sucesso:
        #     self.status = True
        # else:
        #     self.status = False

    def on_exit(self):
        # Este método é chamado quando a máquina de estados está saindo deste estado, normalmente após a execução.
        print("Saindo do ExemploEstadoInicial.")

    def on_error(self, error):
        # Este método é chamado quando ocorre um erro durante a execução deste estado.
        print(f"Erro no ExemploEstadoInicial: {error}")