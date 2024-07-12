import os
import click

@click.command()
@click.option('--aws-access-key-id', prompt='Enter AWS Access Key ID', help='AWS Access Key ID')
@click.option('--aws-secret-access-key', prompt='Enter AWS Secret Access Key', help='AWS Secret Access Key')
@click.option('--aws-default-region', prompt='Enter AWS Default Region', help='AWS Default Region')
@click.option('--aws-account-id', prompt='Enter CodeArtifact Account ID', help='ID of Account AWS')
@click.option('--codeartifact-repository', prompt='Enter CodeArtifact Repository', help='CodeArtifact Repository')
@click.option('--codeartifact-domain', prompt='Enter CodeArtifact Domain', help='CodeArtifact Domain')
@click.option('--output-path', default='set_aws_env.sh', help='Output path for the environment setup script')
def aws_env_setup(aws_access_key_id, aws_secret_access_key, aws_default_region, aws_account_id, codeartifact_repository, codeartifact_domain, output_path):
    env_setup_script = f"""export AWS_ACCESS_KEY_ID={aws_access_key_id}
export AWS_SECRET_ACCESS_KEY={aws_secret_access_key}
export AWS_DEFAULT_REGION={aws_default_region}
export AWS_ACCOUNT_ID={aws_account_id}
export CODEARTIFACT_REPOSITORY={codeartifact_repository}
export CODEARTIFACT_DOMAIN={codeartifact_domain}
"""
    with open(os.path.join(output_path, "aws.sh"), "w") as file:
        file.write(env_setup_script)

    print(f"Run 'source {output_path}' to set the environment variables.")

if __name__ == '__main__':
    aws_env_setup()