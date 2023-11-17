import platform
import os
from invoke import task


@task
def dev(ctx):
    ctx.run("python -m venv venv")
    ctx.run("aws codeartifact login --tool pip --repository wmt-python-rpa-libraries --domain wmt-libraries --domain-owner 435062120355 --region us-east-1")
    ctx.run("pip install -r requirements.txt")


@task
def build(ctx):
    # clean(ctx)
    # Obtenha o valor de PIP_INDEX_URL da função buildspec
    print("esta aqui")
    pip_index_url = buildspec(ctx)
    ctx.run("python setup.py bdist_wheel")
    ctx.run(
        f"docker build -t changeme:v1.0 --build-arg PIP_INDEX_URL={pip_index_url} .")


@task
def buildspec(ctx):
    print("Getting CodeArtifact authorization...")
    # Substitua as variáveis a seguir pelos valores apropriados
    CODEARTIFACT_DOMAIN = 'wmt-libraries'
    AWS_ACCOUNT_ID = '435062120355'
    CODEARTIFACT_REPO = "wmt-python-rpa-libraries"
    AWS_DEFAULT_REGION = "us-east-1"
    authorization_token = ctx.run(
        f"aws codeartifact get-authorization-token --domain {CODEARTIFACT_DOMAIN} --domain-owner {AWS_ACCOUNT_ID} --query authorizationToken --output text", hide=True).stdout.strip()
    PIP_INDEX_URL = f"https://aws:{authorization_token}@{CODEARTIFACT_DOMAIN}-{AWS_ACCOUNT_ID}.d.codeartifact.{AWS_DEFAULT_REGION}.amazonaws.com/pypi/{CODEARTIFACT_REPO}/simple/"
    # Retorne o valor de PIP_INDEX_URL para uso na função build
    print(PIP_INDEX_URL)
    return PIP_INDEX_URL


@task
def test(ctx):
    ctx.run("pytest tests/")
    ctx.run("pytest --docker tests/")


@task
def publish(ctx):
    ctx.run("aws codeartifact login --tool pip --repository wmt-python-rpa-libraries --domain wmt-libraries --domain-owner 435062120355 --region us-east-1")
    ctx.run("aws codeartifact login --tool twine --repository wmt-python-rpa-libraries --domain wmt-libraries --domain-owner 435062120355 --region us-east-1")
    ctx.run("pip install twine")
    ctx.run("python setup.py sdist")
    ctx.run("python -m twine check dist/")
    ctx.run("python -m twine upload --repository codeartifact dist/")


@task
def clean(ctx):
    os_name = platform.system()
    if os_name == "Windows":
        ctx.run("cmd /c rmdir /s /q dist build *.egg-info")
    else:
        ctx.run("rm -rf venv dist build *.egg-info")
