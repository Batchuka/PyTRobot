from config import *
from flask import Flask, request
import threading
import time

app = Flask(__name__)


def run_flask():
    flask_thread = threading.Thread(target=app.run)
    flask_thread.start()
    Bag.flask_server = flask_thread


def shutdown_flask():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug server')
    func()


@app.route('/force_dispatcher', methods=['POST'])
def force_dispatcher():
    # Lógica para forçar o agente a ir para o estado Dispatcher
    # ...
    print('Received force_dispatcher request')
    # return 'Agent forced to Dispatcher state'


@app.route('/receive_assets', methods=['POST'])
def receive_assets():
    json_data = request.get_json()
    # Lógica para processar o JSON de assets
    # ...
    print('Received assets request')
    # return 'Assets received and processed'


@app.route('/receive_params', methods=['POST'])
def receive_params():
    json_data = request.get_json()
    # Lógica para processar o JSON de params
    # ...
    print('Received params request')
    # return 'Params received and processed'


# lógica reservada para testes
if __name__ == '__main__':
    run_flask()
    while True:
        time.sleep(30)
        print("continuo independente...")
