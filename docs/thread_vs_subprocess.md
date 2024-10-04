
# Thread Vs. Subprocess

Resumo:
- Threads são mais indicadas para tarefas que envolvem I/O intensivo, já que permitem uma troca de contexto rápida e baixo consumo de memória.
- Subprocessos são mais indicados para tarefas CPU-bound que exigem paralelismo real, pois não são limitados pelo GIL, e oferecem maior isolamento, tornando-as mais estáveis em caso de falhas.

| **Critério**                    | **Threads**                                                                                               | **Subprocessos**                                                                                               |
| ------------------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Consumo de Memória**          | Menor, pois todas as threads compartilham o mesmo espaço de memória.                                      | Maior, pois subprocessos têm seu próprio espaço de memória.                                                    |
| **Comunicação**                 | Comunicação entre threads é mais rápida, pois compartilham memória.                                       | Comunicação mais lenta, requer IPC (Inter-Process Communication).                                              |
| **Isolamento**                  | Menor isolamento: bugs ou erros em uma thread podem afetar outras.                                        | Maior isolamento: subprocessos são independentes, erros não afetam o processo principal.                       |
| **Controle de Execução**        | Mais fácil de gerenciar e interromper threads diretamente.                                                | Subprocessos são mais difíceis de controlar diretamente (necessita sinalização específica).                    |
| **Desempenho (CPU-bound)**      | Threads são limitadas pelo GIL (Global Interpreter Lock) no Python, especialmente para tarefas CPU-bound. | Subprocessos não são limitados pelo GIL, melhor para tarefas CPU-bound intensivas.                             |
| **Desempenho (I/O-bound)**      | Threads são eficientes para tarefas de I/O, como leitura/escrita de arquivos, rede etc.                   | Subprocessos não trazem benefícios adicionais em relação a threads para I/O.                                   |
| **Estabilidade**                | Threads são mais propensas a erros de concorrência (race conditions).                                     | Subprocessos são mais estáveis devido ao isolamento.                                                           |
| **Facilidade de Implementação** | Threads são mais fáceis de implementar em Python com bibliotecas padrão como `threading`.                 | Subprocessos requerem mais complexidade na criação e controle, especialmente para comunicação entre processos. |
| **Paralelismo Real**            | Threads são limitadas pelo GIL, o que impede paralelismo real em tarefas CPU-bound.                       | Subprocessos permitem paralelismo real, pois cada processo pode rodar em núcleos diferentes.                   |
| **Escalabilidade**              | Escalável para um número razoável de threads (depende da complexidade das tarefas).                       | Escalável para muitas tarefas simultâneas, pois subprocessos são mais isolados e independentes.                |
| **Overhead de Criação**         | Threads têm menor overhead na criação e finalização.                                                      | Subprocessos têm maior overhead devido à inicialização separada de um novo processo.                           |
