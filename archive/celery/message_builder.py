# pytrobot/core/strategy/celery/message_builder.py

import os
import uuid
import json
import socket
import base64

class MessageBuilder:
    
    def __init__(self, task_name, args=None, kwargs=None, eta=None, expires=None, root_id=None, parent_id=None, group_id=None):
        self.task_name = task_name
        self.args = args or []
        self.kwargs = kwargs or {}
        self.eta = eta
        self.expires = expires
        self.task_id = str(uuid.uuid4())
        self.root_id = root_id or self.task_id
        self.parent_id = parent_id
        self.group_id = group_id

    def build(self):
        """Constrói a mensagem no formato esperado pelo protocolo Celery v2"""
        properties = {
            'correlation_id': self.task_id,
            'content_type': 'application/json',
            'content_encoding': 'utf-8',
        }

        headers = {
            'lang': 'py',
            'task': self.task_name,
            'id': self.task_id,
            'root_id': self.root_id,
            'parent_id': self.parent_id,
            'group': self.group_id,
            'eta': self.eta.isoformat() if self.eta else None,
            'expires': self.expires.isoformat() if self.expires else None,
            'retries': 0,
            'argsrepr': repr(self.args),
            'kwargsrepr': repr(self.kwargs),
            'origin': f'{os.getpid()}@{socket.gethostname()}',
        }

        body = [
            self.args,  # Lista de argumentos
            self.kwargs,  # Dicionário de keyword arguments
            {  # Campo embed para callbacks, errbacks, chain e chord
                "callbacks": None,
                "errbacks": None,
                "chain": None,
                "chord": None
            }
        ]

        # Convertendo o body para JSON e depois para base64
        body_json = json.dumps(body)
        body_base64 = base64.b64encode(body_json.encode('utf-8')).decode('utf-8')

        # Montando a mensagem completa
        message = {
            "body": body_base64,
            "headers": headers,
            "properties": properties
        }

        # Convertendo a mensagem final para base64
        message_json = json.dumps(message)
        message_base64 = base64.b64encode(message_json.encode('utf-8')).decode('utf-8')

        return message_base64