# VARIÁVEIS DE AMBIENTE

## Assets via .properties

Para o uso desse framework, você precisa definir os *Assets* em *.properties*. O properties será 'preenchido' de três formas:

1. SSM   → Serviço AWS SSM, onde as variáveis no .properties devem ter o mesmo nome que no serviço;
2. LOCAL → O framework irá considerar os valores que estão no próprio arquivo;

A maneira de parametrizar um ou outro é via variáveis de ambiente! Ou seja, você precisa configurar uma variável de ambiente chamada *PYTROBOT_PROP*

## Modo de execução

Você tem poder para definir o modo de execução de seu robô. Para isso, configure a variável de ambiente *PYTROBOT_ENV* das seguintes maneiras:

- DEV : irá para o fluxo de desenvolvimento;
- OPS : irá para o fluxo de produção.

# SNIPPETS

## Adicionando variável de ambiente

```linux
nano ~/.bashrc
export NOME_DA_VARIAVEL="valor_da_variavel"
source ~/.bashrc
```