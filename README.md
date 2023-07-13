#  PyTRobot — Robô Transacional com Python

## Visão geral

O projeto é um state pattern baseado em Dispatcher e Performer. O objetivo é fornecer um scaffold para uma automação python transacional.

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

