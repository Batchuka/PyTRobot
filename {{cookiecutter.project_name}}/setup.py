from setuptools import setup, find_packages

setup(
    name='{{cookiecutter.project_name}}',
    version='1.0.0',
    author='your-name',
    author_email='your-email',
    description='your-description',
    long_description='',  # Pode ser um arquivo README.md
    # Indica o tipo do conteúdo da long_description
    long_description_content_type='text/markdown',
    url='',  # URL do repositório da biblioteca
    packages=find_packages(),  # Encontra automaticamente todos os pacotes Python do projeto
    install_requires=[
    ]
)
