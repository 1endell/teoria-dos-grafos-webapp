from setuptools import setup, find_packages

setup(
    name='grafo_backend',
    version='0.1.0',
    packages=find_packages(),
    description='Backend library for graph theory studies',
    author='Wendell Bassi',
    author_email='wendellmendes@live.com',
    url='', # Optional
    install_requires=[
        'networkx>=2.6.3',
        'matplotlib>=3.5.1',
        'numpy>=1.21.5',
        'scipy>=1.7.3',
    ],
)
