# test/test_celery_strategy.py
import unittest
from pytrobot.core.strategy.celery.concrete import CeleryStrategy

class TestCeleryStrategy(unittest.TestCase):
    
    def setUp(self):
        # Inicializa a estratégia de Celery antes de cada teste
        self.celery_strategy = CeleryStrategy()
        self.celery_strategy.initialize(
            region_name="us-east-1",
            role_arn="arn:aws:iam::example-role",
            queue_url="https://sqs.us-east-1.amazonaws.com/123456789012/my-queue",
            queue_name="my-queue",
            visibility_timeout=3600,
            polling_interval=10
        )

    def test_start_celery_strategy(self):
        # Testa se a estratégia de Celery pode ser iniciada corretamente
        self.celery_strategy.start()
        self.assertTrue(self.celery_strategy.multithread_manager.get_number_active_threads() > 0)

    def test_stop_celery_strategy(self):
        # Testa se a estratégia de Celery pode ser interrompida corretamente
        self.celery_strategy.start()
        self.celery_strategy.stop()
        self.assertTrue(self.celery_strategy.multithread_manager.get_number_active_threads() == 0)

if __name__ == "__main__":
    unittest.main()
