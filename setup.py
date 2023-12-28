# pytrobot/setup.py
from setuptools import setup, find_packages
from pathlib import Path
from pytrobot.__init__ import __version__

def get_install_requires():
    requirements_path = Path(__file__).parent / "requirements.txt"
    if requirements_path.exists():
        with open(requirements_path, "r") as requirements_file:
            return requirements_file.read().splitlines()
    return []

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
    install_requires=get_install_requires(),
    entry_points={
        'console_scripts': [
            'trt = pytrobot.__init__:program.run',
        ],
    }
)