from setuptools import setup, find_packages

setup(
    name='projeto_aplicado',
    version='0.1',
    packages=find_packages(include=['projeto_aplicado', 'projeto_aplicado.*']),
    install_requires=[],
)