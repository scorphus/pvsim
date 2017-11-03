#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

from pvsim.simulators import PVSimulator
from unittest import TestCase


class PVSimulatorTestCase(TestCase):

    def setUp(self):
        self.pvs = PVSimulator()

    def test_power_at_returns_zero_if_before_sunrise(self):
        two_am = 2 * 3600
        power = self.pvs.power_at(two_am)
        self.assertEqual(power, 0)

    def test_power_at_returns_zero_when_past_sunset(self):
        elevn_pm = 23 * 3600
        power = self.pvs.power_at(elevn_pm)
        self.assertEqual(power, 0)

    def test_power_at_returns_gt_zero_when_light(self):
        noon = 12 * 3600
        power = self.pvs.power_at(noon)
        self.assertGreater(power, 0)
