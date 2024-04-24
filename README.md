# Pytrobot Framework

## Visão Geral
Pytrobot é um framework Python para automação RPA (Robotic Process Automation), projetado com base em uma máquina de estados transacionais. Ele permite a execução de automações robustas e escaláveis, manipulando 'Unidades Fundamentais de Processamento' que são, essencialmente, itens (TransactionItem) de um dataset (TransactionData). O Pytrobot visa oferecer uma experiência de desenvolvimento simplificada, mantendo a flexibilidade para casos de uso complexos e variados.

## Funcionalidades
- **Gerenciamento de Estado**: O Pytrobot utiliza um sistema de máquina de estados para gerenciar o fluxo de automação, permitindo um controle preciso sobre cada etapa do processo. Explore a classe 'StateMachine' e se familiarize com seus atributos.
- **Estados Definidos pelo Usuário**: O usuário deve pensar em seu robô através dos 'Estados' que ele terá. Use a classe 'BaseState' que te fornecerá os métodos abstratos e integrará eles à máquina de estado. Essa classe base também te dará poder para manipular a máquina de estados com o método 'transition'.
- **Dataset de processamento**: O usuário deve pensar na 'carga de processamento' que o robô irá executar, essa carga deve ser iniciada e estruturada em um objeto 'TransactionData', onde cada item é um 'TransactionItem'. Essa classe fornecerá métodos de acesso e controle de processamento. 
- **Objetos únicos com Singleton**: O usuário deve entender que 'TransactionData' e todos os estados que ele implementar não terão múltiplas instancias. Este framework se sustenta no uso do padrão 'Singleton', e usa isso para recuperação dinâmica das classes instaciadas.


## Como Começar
Para começar a usar o Pytrobot, siga os seguintes passos:

1. **Instalação**:
   Instale o Pytrobot usando pip e git (futuramente estará em repo PyPi):
   ```sh
   pip install git+https://github.com/Batchuka/PyTRobot-Framework.git
   ```
2. **Desenvolva**:
    Crie seus próprios estados e defina as transições entre eles. Consulte a documentação para exemplos e padrões recomendados. Use os comandos do Pytrobot CLI
    ```sh
    trt new
    ```

3. **Build**:
    Builde o projeto para um pacote instalável que será automaticamente usado pelo Dockerfile — esse projeto pressupoe ambiente Docker como runtime.
    ```sh
    trt build
    ```

4. **Teste**:
    Recomenda-se fortemente testar os estados com a construção de testes unitários 'Unitest'
    ```sh
    trt testState
    ```


## Documentação

Para obter mais informações sobre como instalar o Pytrobot, configurar estados e transições, e construir sua automação, consulte a [documentação completa](https://github.com/Batchuka/PoG-PyTRobot-framework/wiki).

## Contribuindo

Estamos abertos a contribuições! Se você tem sugestões de melhorias, correções de bugs ou novas funcionalidades, fique à vontade para criar uma pull request ou uma issue.

## Licença

O Pytrobot é distribuído sob a licença MIT. Para mais detalhes, veja o arquivo LICENSE.

## Suporte e Comunidade

Se você precisa de suporte, quer contribuir ou simplesmente se conectar com outros usuários do Pytrobot, visite nossa seção de [issues](https://github.com/Batchuka/PoG-PyTRobot-framework/issues) no GitHub. Aqui, você pode relatar bugs, discutir melhorias, e solicitar novas funcionalidades.

Para orientações detalhadas sobre como contribuir para o projeto, por favor, consulte o arquivo [`CONTRIBUTING.md`](https://github.com/Batchuka/PoG-PyTRobot-framework/blob/main/CONTRIBUTING.md) no repositório. Ele contém todas as informações necessárias para você começar a contribuir, incluindo como criar pull requests, padrões de codificação e como as contribuições são revisadas.

Junte-se a nós para melhorar o Pytrobot e ajudar a comunidade a crescer!

