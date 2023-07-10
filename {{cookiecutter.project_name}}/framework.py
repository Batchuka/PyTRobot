from config import *
from modules import make_settings
from modules import make_control
from modules import make_flask
from modules import make_websocket
from modules import make_sqs
from modules import make_subprocess


@apply_decorator_to_all_methods(handle)
class Starter(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.STARTER

    def on_entry(self):

        # inicie seu dicionário de assets caso não exista
        if Bag.assets is None:
            Bag.assets = make_settings.from_json(Bag.Environment.value)

        # inicie variáveis que precisar nos dicionários
        make_settings.set_aws_profile()

    def execute(self):

        # para garantir a limpeza de arquivos residuais
        make_control.delete_all_temp_files()

        # inicie todas as informações de ambiente
        if Bag.list_of_projects is None:
            make_settings.get_list_projects()

        # inicie todas aplicações que serão utilizadas
        if Bag.sqs_client is None:
            make_sqs.get_client()
        if Bag.websocket_server is None:
            make_websocket.run_websocket()
        # if Bag.flask_server is None:
        #     make_flask.run_flask()

    def on_error(self):

        self.next_state = State.FINISHER

    def on_exit(self):

        self.next_state = State.CONTROLLER


@apply_decorator_to_all_methods(handle)
class Controller(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.CONTROLLER

    def on_entry(self):

        pass

    def execute(self):

        make_control.look_for_transaction_item(self)

    def on_error(self):

        self.next_state = State.FINISHER

    def on_exit(self):

        pass


@apply_decorator_to_all_methods(handle)
class Dispatcher(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.DISPATCHER

    def on_entry(self):

        pass

    def execute(self):

        make_sqs.watch_queue_until_get_one(by_interval=True)

    def on_error(self):

        self.next_state = State.FINISHER

    def on_exit(self):

        self.next_state = State.CONTROLLER


@apply_decorator_to_all_methods(handle)
class Performer(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.PERFORMER

    def on_entry(self):

        pass

    def execute(self):

        # chama o a automação devida
        make_subprocess.launch()

        # após executar automação — correta ou incorretamente — deve apagar o 'input.json'. O item da fila já é excluido na função 'get_queue_item'
        make_control.delete_input_json()

    def on_error(self):

        self.next_state = State.FINISHER

    def on_exit(self):

        self.next_state = State.CONTROLLER


@apply_decorator_to_all_methods(handle)
class Finisher(Robot):

    def __init__(self):
        super().__init__()
        self.current_state = State.FINISHER

    def on_entry(self):

        # se prepare para desligar: salve algo se precisar
        pass

    def execute(self):

        # Feche todas as aplicações, limpe sua bagunça e mande um Log
        make_control.delete_all_temp_files()
        make_control.kill_pending_schedule()
        # make_flask.shutdown_flask()

    def on_error(self):

        print("I shit myself!")
        exit()

    def on_exit(self):

        print("I'll be back!")
        exit()
