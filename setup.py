#!/usr/bin/python
from setuptools import setup, find_namespace_packages

setup(
    name='mlpyqtgraph',
    version='0.1',
    author='Sietze van Buuren',
    author_email='s.van.buuren@gmail.com',
    packages=find_namespace_packages(include=['mlpyqtgraph', 'mlpyqtgraph.*']),
    python_requires=">=3.8",
    package_dir={"mlpyqtgraph": "mlpyqtgraph"},
    url='https://github.com/swvanbuuren',
    license='LICENSE',
    description='Matplotlib like plotting with pyqtgraph in python ',
    long_description=open('README.md').read(),
    install_requires=['pyqtgraph',
                      'PySide2',]
)
