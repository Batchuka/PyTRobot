from celery import Celery, Task
import boto3
from datetime import datetime

class CeleryManager:
    
    def __init__(self, broker_url, result_backend, region_name, role_arn, queue_url, visibility_timeout=3600, polling_interval=10):
        self.broker_url = broker_url
        self.result_backend = result_backend
        self.region_name = region_name
        self.role_arn = role_arn
        self.queue_url = queue_url
        self.visibility_timeout = visibility_timeout
        self.polling_interval = polling_interval
        self.celery_app = Celery('tasks', broker=self.broker_url)
        self.celery_app.conf.result_backend = self.result_backend
        self.celery_app.conf.broker_transport_options = {
            'region': self.region_name,
            'visibility_timeout': self.visibility_timeout,
            'polling_interval': self.polling_interval
        }
        self.sqs_client = self._assume_role_and_get_sqs_client()

    def _assume_role_and_get_sqs_client(self):
        sts_client = boto3.client('sts')
        session_name = f"AssumeRoleSession_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        assumed_role_object = sts_client.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName=session_name,
            DurationSeconds=self.visibility_timeout
        )
        credentials = assumed_role_object['Credentials']
        sqs_client = boto3.client(
            'sqs',
            region_name=self.region_name,
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
        )
        return sqs_client

    def Worker(self, cls):
        task = self.celery_app.task(base=BaseWorker)(cls().run)
        return task

    def add_task(self, worker_cls, *args, **kwargs):
        worker_cls().apply_async(args=args, kwargs=kwargs)

    def run(self):
        self.celery_app.start(argv=['celery', 'worker', '--loglevel=info'])

class BaseWorker(Task):
    abstract = True

    def run(self, *args, **kwargs):
        raise NotImplementedError("O método 'run' deve ser implementado pelo worker.")

if __name__ == "__main__":
    import os

    # Obter credenciais da memória
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

    # Configurar o CeleryManager com os parâmetros necessários
    celery_manager = CeleryManager(
        broker_url='sqs://aws_access_key_id:aws_secret_access_key@',
        result_backend='redis://localhost:6379/0',
        region_name='us-east-1',
        role_arn='arn:aws:iam::435062120355:role/wmt-service-robot-role',
        queue_url='https://sqs.us-east-1.amazonaws.com/435062120355/wmt-declaracao-importacao-queue'
    )

    # Definir e registrar o primeiro worker
    @celery_manager.Worker
    class PrintarValoresWorker(BaseWorker):

        def run(self, param1, param2):
            print(f"Processando {param1} e {param2}")

    # Definir e registrar o segundo worker
    @celery_manager.Worker
    class AcessarSiteWorker(BaseWorker):

        def run(self, url):
            print(f"Acessando o site: {url}")

    # # Adicionar tarefas à fila
    # celery_manager.add_task(PrintarValoresWorker, "dados1", "dados2")
    # celery_manager.add_task(AcessarSiteWorker, "http://example.com")

    # Executar o worker do Celery
    celery_manager.run()
