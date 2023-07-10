from config import *
import asyncio
import threading
import time
import json
import websockets


async def websocket_handler(websocket, path):
    if path == "/controller":
        await handle_controller(websocket)
    elif path == "/config":
        await handle_config(websocket)
    else:
        await handle_default(websocket)


async def handle_controller(websocket):

    async for message in websocket:

        # Lógica para processar mensagens de chat
        if message.startswith('{"assets":'):

            try:
                data = json.loads(message)
                command = data['command']
                # Acessar outros campos do JSON conforme necessário

                if command == 'set_asset':
                    # Lógica para processar o comando 'set_asset'
                    # ...

                    # Preparar e enviar uma resposta de volta ao cliente
                    response = "Comando 'set_asset' processado com sucesso"
                else:
                    response = "Comando desconhecido"

            except json.JSONDecodeError:
                response = "Erro de decodificação do JSON"

        else:
            response = f"Que???! Tá errado, você é burro!"

        await websocket.send(response)


async def handle_config(websocket):
    async for message in websocket:

        # Lógica para processar mensagens de chat
        if message == 'assets':
            message = Bag.assets
            # Preparar e enviar uma resposta de volta ao cliente
            response = f"As configurações atuais são: {message}"

        elif message == 'pid':
            message = Bag.pid
            # Preparar e enviar uma resposta de volta ao cliente
            response = f"O PID atual é: {message}"

        elif message == 'transaction_item':
            message = Bag.transaction_item
            # Preparar e enviar uma resposta de volta ao cliente
            response = f"A transação atual é: {message}"

        elif message == 'list_of_projects':
            message = Bag.list_of_projects
            # Preparar e enviar uma resposta de volta ao cliente
            response = f"Os projetos que posso rodar são: {message}"

        else:
            response = f"Esse comando não existe seu animal! Tá errado!"

        await websocket.send(response)


async def handle_default(websocket):
    async for message in websocket:
        # Lógica para tratamento padrão
        response = """Fala ai burro! Vou te explicar como funciona:

Você pode usar os seguintes caminhos para acessar diferentes recursos:

- /controller: Use esse caminho para enviar comandos de controle. O formato JSON esperado para os comandos é: {"assets": ...}.
  Comandos suportados: "set_asset".

- /config: Use esse caminho para obter informações de configuração.
  Comandos suportados: "assets", "pid", "transaction_item", "list_of_projects".

Para acessar um recurso, conecte-se ao caminho correspondente usando um cliente WebSocket."""

        await websocket.send(response)


def run_websocket():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(websocket_handler, "192.168.1.84", 8333)
    loop.run_until_complete(start_server)
    loop.run_forever()


# Lógica reservada para testes
if __name__ == '__main__':

    Bag.assets = {
        'sqs_queue_url': "https://sqs.us-east-1.amazonaws.com/435062120355/wmt-consultas-due-dilligence.fifo",
        'sqs_queue_region': "us-east-1",
        'medium_sleep': 5,
        'large_sleep': 10,
        'max_number_of_messages_queue': 1,
        'wait_time_seconds': 10
    }

    Bag.list_of_projects = ['wmt-005', 'wmt-006']

    Bag.transaction_item = {'message_id': 159159, 'value': "conclusão"}

    pid = 185648
    websocket_thread = threading.Thread(target=run_websocket)
    websocket_thread.start()

    while True:

        pid += 1
        Bag.pid = pid

        print("inicio")
        time.sleep(5)
        print("fim")
