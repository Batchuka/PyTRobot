# pytrobot/subprocess_feature.py

import subprocess as sp
from pytrobot.core.singleton import Singleton

class SubprocessManager(metaclass=Singleton):
    def __init__(self):
        self.processes = {}

    def executar_subprocesso(self, comando, captura_saida=True, captura_erro=True):
        """
        Método para executar um subprocesso com captura de saída e erro.

        Args:
            comando (list): Lista de strings contendo o comando a ser executado.
            captura_saida (bool, opcional): Indica se a saída padrão do subprocesso deve ser capturada (padrão: True).
            captura_erro (bool, opcional): Indica se a saída de erro do subprocesso deve ser capturada (padrão: True).

        Returns:
            dict: Dicionário contendo os seguintes campos:
                sucesso (bool): Indica se o subprocesso foi executado com sucesso.
                saida (str, opcional): Saída padrão do subprocesso (se `captura_saida` for True).
                erro (str, opcional): Saída de erro do subprocesso (se `captura_erro` for True).
                codigo_saida (int): Código de saída do subprocesso.
        """
        try:
            # Crie um identificador único para o subprocesso
            process_id = f"process_{len(self.processes) + 1}"
            
            # Execute o subprocesso
            processo = sp.Popen(comando, stdout=sp.PIPE if captura_saida else sp.DEVNULL, stderr=sp.PIPE if captura_erro else sp.DEVNULL)
            self.processes[process_id] = processo

            # Capture a saída e o erro
            saida, erro = processo.communicate()

            # Decode a saída e o erro para strings
            saida = saida.decode('utf-8') if captura_saida else None
            erro = erro.decode('utf-8') if captura_erro else None

            # Verifique o código de saída
            codigo_saida = processo.returncode

            # Determine se o subprocesso foi executado com sucesso
            sucesso = codigo_saida == 0

            # Remova o processo do registro após a conclusão
            del self.processes[process_id]

            return {'process_id': process_id, 'saida': saida, 'sucesso': sucesso, 'erro': erro, 'codigo_saida': codigo_saida}

        except Exception as e:
            # Capture o erro em caso de falha
            erro = f"Erro ao executar o subprocesso: {e}"
            sucesso = False
            return {'process_id': None, 'saida': None, 'sucesso': sucesso, 'erro': erro, 'codigo_saida': -1}

    def list_active_processes(self):
        """
        Lista todos os subprocessos ativos gerenciados pelo SubprocessManager.
        """
        active_processes = {pid: proc for pid, proc in self.processes.items() if proc.poll() is None}
        print(f"Active processes count: {len(active_processes)}")
        for pid, proc in active_processes.items():
            print(f"Process ID: {pid}, Process PID: {proc.pid}")

    def stop_process(self, process_id):
        """
        Finaliza o subprocesso associado ao ID fornecido.
        """
        if process_id in self.processes:
            proc = self.processes[process_id]
            if proc.poll() is None:
                print(f"Terminating the process {process_id}.")
                proc.terminate()
            else:
                print(f"Process {process_id} is no longer active.")
        else:
            print(f"No process found with ID {process_id}.")


# Decorator
def Subprocess(comando, captura_saida=True, captura_erro=True):
    """
    Função para acessar o SubprocessManager do PyTRobot e executar um subprocesso.
    
    Args:
        comando (list): Lista de strings contendo o comando a ser executado.
        captura_saida (bool, opcional): Indica se a saída padrão do subprocesso deve ser capturada (padrão: True).
        captura_erro (bool, opcional): Indica se a saída de erro do subprocesso deve ser capturada (padrão: True).

    Returns:
        dict: Resultado do subprocesso, conforme retornado pelo SubprocessManager.
    """
    return PyTRobot.set_subprocess(comando, captura_saida, captura_erro)
