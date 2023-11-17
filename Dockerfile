# Use a imagem do Selenium como base
FROM selenium/standalone-firefox:latest

# Exponha as portas necessárias
EXPOSE 4444 7900

# Defina o diretório de trabalho para /home/seluser
WORKDIR /home/seluser

USER root

# Instale pacotes essenciais (se necessário para o seu projeto)
RUN apt-get update && \
    apt-get install -y tar gzip python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir awscli

# this needs to be added before your pip install line!
ARG PIP_INDEX_URL

# Copie o conteúdo do diretório 'dist' para o contêiner
COPY dist /home/seluser/dist

# Instale todos os arquivos do diretório 'dist'
RUN pip install /home/seluser/dist/*

# Copie o conteúdo do diretório 'dist' para o contêiner
COPY run.sh /home/seluser/

# Executar o script 'run.sh' quando o contêiner for iniciado
CMD ["/bin/bash", "/home/seluser/run.sh"]