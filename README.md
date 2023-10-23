#  PyTRobot — Robô Transacional com Python

## Visão geral
---

O projeto é um state pattern baseado em Dispatcher e Performer. O objetivo é fornecer um scaffold para uma automação python transacional.

## Estados
---

O robô possui cinco estados: **Stater**, **Handler**, **Publisher**, **Performer**, **Finisher**;

Cada um desses estados implementa a superclasse *Robot*, por isso recomendo que passe um tempo identificando como ela funciona. Além de ser classe mãe, que abriga o construtor:

- ***status***: quando alguma exceção ocorre, ela é armazenada nesse atributo que é boolean. Essa informação é usada para controlar o fluxo do robô;
- ***current_state***: este atributo é definido pela classe que o herda. Cada instancia deve assinar esse atributo com seu próprio estado;
- ***next_state***: este atributo é determinado pelos métodos 'on_exit()' e 'on_error()' de cada instância que herda 'Robot'. Defina o próximo estado conforme sua necessidade;

ela também é classe estática que abriga os atributos:

- ***transaction_number***: usado para armazenar o número da transação corrente globalmente;
- ***transaction_item***: usado para conter a unidade transacional corrente globalmente;
- ***transaction_data***: usado para armazenar todas as unidades transacionais que devem ser processadas no job;


## State
---



## Common
---


