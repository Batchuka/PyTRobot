from setuptools import setup, find_packages
from pathlib import Path
from __init__ import __version__

setup(
    name='pytrobot',
    version=__version__,
    author='Batchuka',
    author_email='https://github.com/Batchuka',
    long_description=(Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown',
    url='https://github.com/Batchuka/PoG-PyTRobot-framework',
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=[
        "boto3",
        "pandas"
    ],
    entry_points={
        'console_scripts': [
            'trt = pytrobot.__main__:entrypoint',
        ],
    }
)
