from config import *
import boto3
import time
import schedule
import os


@fill_arguments_from_bag
def get_client(sqs_queue_region=None):
    """
    Essa função irá guardar o cliente sqs na Bag para utilização em qualquer contexto

    Args:
        _sqs_queue_region (str, opcional): A região para o cliente SQS. Se não for fornecido, será buscado de Bag.params se _debugger_mode for False.
        _debugger_mode (bool, opcional): Indica se o modo de depuração está ativado. Se não for fornecido, será buscado de Bag.params se _debugger_mode for False.

    Returns:
        None
    """

    # obtém o cliente pela região
    Bag.sqs_client = Bag.aws_session.client('sqs', sqs_queue_region, )


@fill_arguments_from_bag
def watch_queue_until_get_one(large_sleep=None,
                              medium_sleep=None,
                              by_interval=False,
                              by_loop=False):
    """
    Estabelece duas formas de consulta na fila: por intervalo ou por loop. Por intervalo, uma thread a parte será criada para chamar a função _get_queue_item.
    Essa chamada não interrompe o Agente, ele continuará normalmente após schedule. Por loop, ele entra em um laço que só é interrompido quando um item é encontrado.
    Um dos modos deve ser indicado, pois ambos são normalmente falsos.


    Args:
        * _message_group_id (str): O ID do grupo de mensagens da fila — utilizado pela função '_get_queue_item'
        * _large_sleep (int, opcional): O intervalo de sono em minutos para o modo 'by_interval'. Se não for fornecido, será buscado de Bag.params se _debugger_mode for False.
        * _medium_sleep (int, opcional): O intervalo de sono em segundos para o modo 'by_loop'. Se não for fornecido, será buscado de Bag.params se _debugger_mode for False.
        * by_interval (bool, opcional): Indica se o modo de observação é baseado em um intervalo de tempo. Se for True, a função usará o agendador 'schedule' para executar a função '_get_queue_item' em intervalos regulares. O valor padrão é False.
        * by_loop (bool, opcional): Indica se o modo de observação é baseado em um loop contínuo. Se for True, a função executará a função '_get_queue_item' repetidamente até encontrar um item na fila ou atingir uma condição de parada. O valor padrão é False.
        * _debugger_mode (bool, opcional): Indica se o modo de depuração está ativado. Se for True, os valores de '_large_sleep' e '_medium_sleep' não serão buscados de Bag.params. O valor padrão é False.

    Returns:
        None
    """

    if by_interval:

        # de início tenta encontrar
        get_queue_item()

        # se não encontrar, schedula uma pesquisa a cada 'large_sleep' minutos
        if not Bag.transaction_item:
            schedule.every(large_sleep).minutes.do(get_queue_item)

    elif by_loop:

        while True:
            get_queue_item()
            if Bag.transaction_item:
                print("New item found in the queue!")
                break
            else:
                print("No items in the queue yet...")
                time.sleep(medium_sleep)

    else:
        print("Both, by_interval and by_loop are false!")


@fill_arguments_from_bag
def get_queue_item(message_group_id=None,
                   sqs_queue_url=None,
                   max_number_of_messages_queue=None,
                   wait_time_seconds=None,
                   list_of_itens=False):
    """
    Obtém um item da fila ou uma lista de itens da fila, dependendo dos parâmetros fornecidos.

    Args:
        * _message_group_id (str): O ID do grupo de mensagens da fila.
        * _queue_url (str, opcional): A URL da fila a ser consultada. Se não for fornecido, será buscado de Bag.assets se _debugger_mode for False.
        * _max_number_of_messages (int, opcional): O número máximo de mensagens a serem recebidas. Se não for fornecido, será buscado de Bag.params se _debugger_mode for False. Se _list_of_items for True, o valor padrão é 10.
        * _wait_time_seconds (int, opcional): O tempo de espera em segundos para receber mensagens. Se não for fornecido, será buscado de Bag.params se _debugger_mode for False.
        * _list_of_items (bool, opcional): Indica se deseja retornar uma lista de itens da fila em vez de um único item. O valor padrão é False.
        * _debugger_mode (bool, opcional): Indica se o modo de depuração está ativado. Se for True, os valores de '_queue_url', '_max_number_of_messages' e '_wait_time_seconds' não serão buscados de Bag.assets e Bag.params. O valor padrão é False.

    Returns:
        * None se _list_of_items for False
        * ou uma lista de itens da fila se _list_of_items for True.

    Raises:
        Exception: Se ocorrer um erro ao obter o item da fila.
    """

    # montado lista de argumentos
    _request_args = {
        # url da fila a ser consultada
        'QueueUrl': sqs_queue_url,
        # atributos para retornar o grupo da mensagem
        'AttributeNames': ['MessageGroupId'],
        # defina o número máximo de mensagens a serem recebidas
        'MaxNumberOfMessages': max_number_of_messages_queue,
        # defina o tempo de espera para receber mensagens
        'WaitTimeSeconds': wait_time_seconds,
    }

    # adicionando argumento para delete
    if message_group_id:
        # defina o 'MessageGroupId' para puxar mensagens — só interessa para delete
        _request_args['MessageGroupId'] = message_group_id

    # faz a requisição propriamente dita
    _response = Bag.sqs_client.receive_message(**_request_args)

    # se retornar algo e não tiver sido solicitada a lista de itens
    if _response and not list_of_itens:

        # verifica se 'Messages' está presente no dicionário
        if 'Messages' in _response:

            # vamos processar o retorno e adicionar corretamente em 'transaction_item'
            _prepare_transaction_item(_response)

            # após pegar o item, delete ele imediatamente
            if Bag.transaction_item:
                delete_queue_item()

        else:
            # Não há itens na fila
            print("Queue is empty")

    # se retornar algo e tiver sido solicitada a lista
    elif _response and list_of_itens:

        # verifica se 'Messages' está presente no dicionário
        if 'Messages' in _response:

            # retorna a lista completa
            return _response

        else:
            # Não há itens na fila
            return []

    else:
        raise Exception("Error on get_queue_item")


@fill_arguments_from_bag
def delete_queue_item(sqs_queue_url=None):
    # obtem todas as mensagens da fila atual
    _response = get_queue_item(
        list_of_itens=True, max_number_of_messages_queue=10)

    if _response:
        # Extrair o conteúdo do atributo 'body' do JSON de origem
        _receipt_handle = _prepare_message_receipt(
            list_of_itens=_response, message_id=Bag.transaction_item['message_id']
        )

        # chama o cliente para deletar a mensagem
        Bag.sqs_client.delete_message(
            QueueUrl=sqs_queue_url,
            ReceiptHandle=_receipt_handle
        )

    else:
        # Não há itens na fila
        print("Queue is empty")


@fill_arguments_from_bag
def _prepare_transaction_item(response):

    # Extrair o MessageId
    _message_id = response['Messages'][0]['MessageId']

    # Extrair o conteúdo do atributo 'body' do JSON de origem
    _body = response['Messages'][0]['Body']

    # Extrair o valor do atributo 'idRobo' do JSON de origem
    _project_name = response['Messages'][0]['Attributes']['MessageGroupId']

    # Construir o caminho completo do arquivo
    _file_name = "input.json"
    _file_path = os.path.join(os.getcwd(), "temp", _file_name)

    # Gravar o conteúdo do atributo 'body' em um arquivo input.json
    try:
        with open(_file_path, "w") as file:
            file.write(_body)
            print(_body)
        print(f"Transaction item converted on: {_file_path}")
    except IOError as e:
        raise Exception(f"Failed to convert transaction item: {str(e)}")

    # Retornar o dicionário com as colunas idRobo e inputJson
    Bag.transaction_item = {'message_id': _message_id,
                            'project_name': _project_name,
                            'input_json': _file_path}


@fill_arguments_from_bag
def _prepare_message_receipt(list_of_itens,
                             message_id=None):

    _updated_list = list_of_itens['Messages']

    _item_found = list(
        filter(lambda x: x['MessageId'] == message_id, _updated_list))

    _receipt_handle = _item_found[0]['ReceiptHandle']

    return _receipt_handle


# trecho usado para testes
if __name__ == "__main__":

    # preencha assets com parâmetros
    Bag.assets = {
        'sqs_queue_url': "https://sqs.us-east-1.amazonaws.com/435062120355/wmt-agente-onpremise-dev.fifo",
        'sqs_queue_region': "us-east-1",
        'medium_sleep': 5,
        'large_sleep': 10,
        'max_number_of_messages_queue': 1,
        'wait_time_seconds': 10,
        "aws_access_key_id": "-",
        "aws_secret_access_key": "-",
    }

    Bag.aws_session = boto3.Session(
        aws_access_key_id=Bag.assets['aws_access_key_id'],
        aws_secret_access_key=Bag.assets['aws_secret_access_key'],
        region_name=Bag.assets['sqs_queue_region'])

    get_client()

    watch_queue_until_get_one(by_interval=True, large_sleep=0.5)

    counter = 0

    while True:
        schedule.run_pending()
        time.sleep(1)
        counter += 1
        print("Aguardando... Contador:", counter)

        # Faça aqui a lógica para verificar se o item foi encontrado na fila
        if Bag.transaction_item:
            print("Item encontrado!")
            break

    # delete_queue_item()
