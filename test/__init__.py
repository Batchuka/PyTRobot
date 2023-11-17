# testes/conftest.py
import pytest

# Suponha que você queira inicializar um banco de dados de teste antes de todos os testes

# leia a documentação do pytest para entender os parâmetros dessa fixture


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Código de inicialização do banco de dados de teste
    print("Inicializando banco de dados de teste...")
    # Retorne qualquer coisa que você queira fazer disponível nos testes
    yield
    # Código para limpar o banco de dados após todos os testes serem executados
    print("Limpando banco de dados de teste...")


"""

>> Por que não precisa importar o pytest:

O pytest faz uso do mecanismo de descoberta de testes do Python, então você não
precisa importar explicitamente o pytest nos arquivos de teste. O pytest procura 
por padrões específicos nos nomes dos arquivos e nas definições das funções para 
identificar testes. Isso é parte do que torna a estrutura do pytest tão elegante 
e limpa.

Se você seguir as convenções de nomenclatura (por exemplo, prefixar nomes de funções 
de teste com test_) e manter os arquivos de teste no mesmo diretório do código que 
eles estão testando, o pytest os encontrará automaticamente e executará os testes.

Lembre-se de que você ainda precisa do import pytest quando desejar usar recursos 
específicos do pytest, como fixtures ou marcadores personalizados, em seus arquivos 
de teste. Mas para a descoberta básica e a execução de testes, você não precisa 
importar o pytest explicitamente.

>> Fixture no pytest:

Uma fixture no pytest é um objeto ou uma função que você define para fornecer um 
estado pré-determinado para seus testes. Ela permite que você isole parte do código 
que você deseja testar, garantindo que as condições iniciais sejam sempre consistentes 
e controladas.

Por exemplo, imagine que você tem um conjunto de testes que precisa acessar um 
banco de dados. Em vez de criar uma conexão de banco de dados em cada teste, 
você pode criar uma fixture que inicializa a conexão uma vez e a fornece a todos 
os testes que precisam dela.

"""
