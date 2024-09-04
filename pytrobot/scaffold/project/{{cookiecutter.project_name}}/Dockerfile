# Use a imagem do Selenium        ↓ aqui você pode escolher a versão que quiser
FROM selenium/standalone-chrome:latest

# Expondo portas necessárias do Selenium
EXPOSE 4444 7900

# Defina o diretório de trabalho para /home/seluser
WORKDIR /home/seluser

# Instale pacotes essenciais (se necessário para o seu projeto)
RUN apt-get update && \
    apt-get install -y tar gzip python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# instalando o CLI da AWS
RUN pip install --no-cache-dir awscli

# Configurar as credenciais do AWS CodeArtifact
RUN aws codeartifact login --tool pip --repository wmt-python-rpa-libraries --domain wmt-libraries --domain-owner 435062120355 --region us-east-1

# Comando para executar o código do arquivo "main.py" como um módulo Python
CMD ["python3", "-m", ""]
