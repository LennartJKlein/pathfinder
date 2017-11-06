# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='Pathfinder',
    version='0.1.0',
    description='A program that uses wires to connect gates on a chip efficiently.',
    long_description=readme,
    author='Jurre Brandsen, Lennart Klein, Thomas de Lange',
    author_email='info@lennartklein.nl',
    url='https://github.com/LennartJKlein/pathfinder',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
