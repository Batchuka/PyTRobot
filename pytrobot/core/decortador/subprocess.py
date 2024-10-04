# pytrobot/core/decortador/subprocess.py
from pytrobot.core.feature.subprocess import SubprocessManager

def Subprocess(comando, captura_saida=True, captura_erro=True):
    """
    Função para acessar o SubprocessManager diretamente e executar um subprocesso.
    
    Args:
        comando (list): Lista de strings contendo o comando a ser executado.
        captura_saida (bool, opcional): Indica se a saída padrão do subprocesso deve ser capturada (padrão: True).
        captura_erro (bool, opcional): Indica se a saída de erro do subprocesso deve ser capturada (padrão: True).

    Returns:
        dict: Resultado do subprocesso, conforme retornado pelo SubprocessManager.
    """
    subprocess_manager = SubprocessManager()
    return subprocess_manager.executar_subprocesso(comando, captura_saida, captura_erro)
