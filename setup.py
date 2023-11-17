from setuptools import setup, find_packages
from pathlib import Path
from setecutilities import __version__

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
    install_requires=[]
)
