# Use a imagem ECS-optimized Amazon Linux 2 como base
FROM public.ecr.aws/amazonlinux/amazonlinux:2023

# Instala pacotes essenciais (se necessário para o seu projeto)
RUN yum -y update && \
    yum -y install python3 python3-pip tar



# Instale o navegador web e o driver correspondente (por exemplo, Chrome e ChromeDriver)
# Certifique-se de que o driver esteja no PATH
# No exemplo abaixo, estamos usando o ChromeDriver para o Chrome
RUN apt-get update && \
    apt-get install -y wget unzip && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable=115.0.5790.102-1 && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/94.0.4606.41/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip


# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para o diretório de trabalho do container
COPY . /app

# Instala as dependências do projeto (se você tem um requirements.txt)
RUN pip3 install --no-cache-dir -r requirements.txt

# Define o comando padrão a ser executado ao iniciar o container
CMD ["python3", "seu_script.py"]
