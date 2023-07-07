import socket
import threading


def start_agent_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Defina o endereço e porta desejados
    server_socket.bind(('localhost', 8000))
    server_socket.listen(1)

    print("Agente: Servidor de socket iniciado.")

    while True:
        client_socket, address = server_socket.accept()
        print("Agente: Conexão estabelecida com o Jenkins em", address)
        threading.Thread(target=handle_client, args=(client_socket,)).start()


def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        log_message = data.decode()
        print("Agente: Mensagem recebida:", log_message)
        # Faça o que desejar com a mensagem de log, por exemplo, envie para o seu sistema de registro de logs

    client_socket.close()


def send_log_message(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Defina o endereço e porta correspondentes ao servidor do agente
    client_socket.connect(('localhost', 8000))

    print("Jenkins: Conexão estabelecida com o agente.")

    client_socket.sendall(message.encode())
    client_socket.close()


# lógica reservada para testes
if __name__ == '__main__':
    # threading.Thread(target=start_agent_server).start()

    # # Exemplo de uso: enviar uma mensagem de log
    # log_message = "Mensagem de log do Jenkins"
    # send_log_message(log_message)

    # Aqui você pode adicionar mais lógica para o seu agente e interagir com o servidor Flask, etc.
    # Certifique-se de que o script continue sendo executado em algum loop ou aguarde eventos relevantes.
