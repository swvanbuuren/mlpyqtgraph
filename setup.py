#!/usr/bin/python
from setuptools import setup, find_packages

setup(
    name='mlpyqtgraph',
    version='0.1',
    author='Sietze van Buuren',
    author_email='s.van.buuren@gmail.com',
    packages=find_packages(),
    url='https://github.com/swvanbuuren',
    license='LICENSE',
    description='Matplotlib/matlab like pyqtgraph',
    long_description=open('README.md').read(),
    install_requires=['PySide2',
                      'shiboken2',
                      'pyqtgraph']
)
