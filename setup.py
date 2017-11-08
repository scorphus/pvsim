#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

from setuptools import setup, find_packages
from pvsim import __version__

tests_require = [
    'flake8',
    'ipdb',
    'mock',
    'pytest',
    'pytest-cov',
    'sphinx',
    'tox',
]

setup(
    name='pvsim',
    version=__version__,
    description='PV Simulator Challenge',
    long_description='''
PV Simulator Challenge
''',
    keywords='photovoltaic simulator power consumption',
    author='Pablo Santiago Blum de Aguiar',
    author_email='pablo.aguiar@gmail.com',
    url='https://github.com/scorphus/pvism',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
        'pika',
        'toml',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            'pvsim=pvsim.main:main',
        ],
    },
)
