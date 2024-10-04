# Use a imagem do Selenium        ↓ aqui você pode escolher a versão que quiser
FROM selenium/standalone-chrome:#118.0

USER root

EXPOSE 7900

# Configurações do CodeArtifact — Só irá funcionar se publicar o pacote lá!
ARG CODEARTIFACT_REPOSITORY_URL

# Defina o diretório de trabalho para /home/seluser
WORKDIR /home/seluser

# Atualiza o apt e adiciona repositório para Python
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update

# Instala Python 3.11 e suas dependências
RUN apt-get update && apt-get install -y \
    python3.11 python3-pip python3.11-venv python3.11-dev python3.11-tk \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# Reinstala pip para corrigir dependências
RUN python3.11 -m ensurepip --upgrade

# Instalar coisas necessárias para gerenciar projeto
RUN python3.11 -m pip install --upgrade pip setuptools wheel build

# Instalar o CLI da AWS
RUN python3.11 -m pip install --no-cache-dir awscli

# Limpa os arquivos temporários de instalação para reduzir o tamanho da imagem
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Criar um ambiente virtual
RUN python3.11 -m venv venv

# Ativa o ambiente virtual e instala o seu pacote e dependências
RUN /home/seluser/venv/bin/pip install --upgrade pip
RUN /home/seluser/venv/bin/pip config set global.extra-index-url $CODEARTIFACT_REPOSITORY_URL
RUN /home/seluser/venv/bin/pip install {{cookiecutter.project_name}}

# Copiar configuração adicional do Supervisor
COPY {{cookiecutter.project_name}}.conf /etc/supervisor/conf.d/{{cookiecutter.project_name}}.conf

# Retornar o usuário seluser
USER seluser