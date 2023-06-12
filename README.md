#  Agente de robôs On-Premises

## Visão geral

O objetivo desse projeto é construir uma automação capaz de buscar itens em uma fila SQS e passar esse item como *input.json* para um determiando projeto na mesma máquina. Esse agente, portanto, é responsável por iniciar outras automações. Isso é necessário para impedir diferentes robôs de executarem ao mesmo tempo, devendo o agente promover isso a partir da fila SQS.

O agente *schedula* buscas na fila a depender dos valores configurados no *params.json*. Quando uma dessas buscas retorna um item da fila, o robô chama a respectiva automação passando o item como *input.json*. A automação invocada é feita com *subprocess*, o que implica que o agente aguarda a finalização da automação — impedindo-o de invocar outra. 

O agente é munido de um servidor flask que pode implementar funções de controle. Atualmente as funções implementadas são para setup dos arquivos *params.json* e *assets.json*. Futuramente, haverá uma função que força o encerramento de uma automação em andamento.

## Executando o projeto

O projeto é implementado para ser executado em um ambiente on-premises linux em conjuto com um serviço *Jenkins*. Este é responsável por fazer o build e deploy do agente. Logo, sua execução **Depende** do *Jenkins*.

Esse projeto possui dois scripts na pasta *docs*:

> obs: esses arquivos estão na pasta do projeto apenas para documentação. Seu uso é feito através do dashboard Jenkins.

- delivery.jenkinsfile — utilizado para build e deploy do projeto;
- launch.jenkinsfile — utilizado para iniciar execução do projeto na máquina.

Ao final do deploy, o agente é iniciado automaticamente, mas caso não seja o script de launch pode ser empregado. 


## Dependências globais

- É necessário configurar um serviço Jenkins
- É necessário configurar filas no AWS SQS
- É necessário configurar Access Keys de um IAM AWS configuradas no ambiente

