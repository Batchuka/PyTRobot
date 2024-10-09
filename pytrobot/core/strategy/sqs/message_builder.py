# pytrobot\core\strategy\sqs\message_builder.py

import json
from typing import List, Dict, Optional

class SQSMessage:
    def __init__(self, task_name: str, args: List, kwargs: Dict, callback: Dict, metadata: Dict):
        """
        Inicializa a mensagem SQS com os atributos necessários.
        
        :param task_name: Nome da task a ser executada.
        :param args: Lista de argumentos para a task.
        :param kwargs: Argumentos chave-valor para a task.
        :param callback: Dados relacionados ao callback da task.
        :param metadata: Metadados adicionais da task.
        """
        self.task_name = task_name
        self.args = args
        self.kwargs = kwargs
        self.callback = callback
        self.metadata = metadata

    def to_dict(self) -> Dict:
        """
        Converte a mensagem para um dicionário utilizável pelo SQS.
        
        :return: Dicionário contendo a mensagem.
        """
        return {
            'task_name': self.task_name,
            'args': self.args,
            'kwargs': self.kwargs,
            'callback': self.callback,
            'metadata': self.metadata
        }

    def to_json(self) -> str:
        """
        Converte a mensagem para um formato JSON.
        
        :return: String JSON da mensagem.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)

class SQSMessageBuilder:
    def __init__(self, task_name: str):
        """
        Inicializa o builder com o nome da task.
        
        :param task_name: O nome da task que será executada.
        """
        self.task_name = task_name
        self.args = []
        self.kwargs = {}
        self.callback = {}
        self.metadata = {}

    def add_args(self, *args: List) -> 'SQSMessageBuilder':
        """
        Adiciona uma lista de argumentos à task.
        
        :param args: Lista de argumentos para a task.
        :return: Instância atualizada de SQSMessageBuilder.
        """
        self.args.extend(args)
        return self

    def add_kwargs(self, **kwargs) -> 'SQSMessageBuilder':
        """
        Adiciona argumentos com palavras-chave à task.
        
        :param kwargs: Argumentos chave-valor para a task.
        :return: Instância atualizada de SQSMessageBuilder.
        """
        self.kwargs.update(kwargs)
        return self

    def set_callback(self, url: str, auth_token: str, method: str = 'POST', headers: Optional[Dict] = None) -> 'SQSMessageBuilder':
        """
        Define os dados para o callback.
        
        :param url: URL para qual a resposta deve ser enviada.
        :param auth_token: Token de autenticação para validar o callback.
        :param method: Método HTTP (padrão: POST).
        :param headers: Headers HTTP adicionais para a requisição (opcional).
        :return: Instância atualizada de SQSMessageBuilder.
        """
        self.callback = {
            'url': url,
            'auth_token': auth_token,
            'method': method,
            'headers': headers or {}
        }
        return self

    def set_metadata(self, task_id: str, priority: str = 'medium', retries: int = 0, expires_at: Optional[str] = None) -> 'SQSMessageBuilder':
        """
        Define os metadados para a task.
        
        :param task_id: ID único da task.
        :param priority: Prioridade da task (low, medium, high).
        :param retries: Número de tentativas em caso de falha.
        :param expires_at: Data de expiração da mensagem (ISO 8601).
        :return: Instância atualizada de SQSMessageBuilder.
        """
        self.metadata = {
            'task_id': task_id,
            'priority': priority,
            'retries': retries,
            'expires_at': expires_at
        }
        return self

    def build(self) -> SQSMessage:
        """
        Constrói e retorna uma instância de SQSMessage.
        
        :return: Instância de SQSMessage.
        """
        return SQSMessage(
            task_name=self.task_name,
            args=self.args,
            kwargs=self.kwargs,
            callback=self.callback,
            metadata=self.metadata
        )