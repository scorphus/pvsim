#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

import csv
import sys


class Writer(object):

    def write(self, data):
        raise NotImplementedError('write should be implemented by subclass')


class StdoutWriter(Writer):

    def write(self, data):
        sys.stdout.write('{}'.format(data))


class CSVWriter(Writer):

    def __init__(self, filepath):
        self.filepath = filepath

    def write(self, data):
        with open(self.filepath, 'a') as fp:
            csv_writer = csv.writer(fp)
            csv_writer.writerow(data)
