#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>


import sys
from argparse import ArgumentParser


class ArgParser(object):

    def __init__(self):
        self._parser = ArgumentParser(
            prog='pvsim', description='PV Simulator Challenge', add_help=False
        )
        self._add_arguments()

    def _add_arguments(self):
        self._parser.add_argument(
            '-c', '--config',
            type=str,
            nargs=1,
            default='config.toml',
            help='path for configuration file',
        )
        self._parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='activate verbose mode',
        )
        self._parser.add_argument(
            '--version',
            action='store_true',
            help='display program version',
        )
        self._parser.add_argument(
            '-h', '--help',
            action='store_true',
            help='display this help message',
        )
        self._parser.add_argument(
            'action',
            nargs='?',
            help='either one of `meter´, `simulator´ or `plot´',
        )

    def parse(self):
        return self._parser.parse_args()

    def print_help(self):
        self._parser.print_help(sys.stderr)

    def print_usage(self):
        self._parser.print_usage(sys.stderr)

    def print_version(self, version):
        sys.stderr.write('pvsim {}'.format(version))
