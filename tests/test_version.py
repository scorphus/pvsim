#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

from pvsim import __version__
from unittest import TestCase


class VersionTestCase(TestCase):

    def test_has_proper_version(self):
        self.assertEqual(__version__, '0.1.0')
