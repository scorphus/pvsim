#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

from math import pi
from mock import patch
from pvsim.simulators import PVSimulator, Simulator
from unittest import TestCase


class SimulatorTestCase(TestCase):

    def setUp(self):
        self.pcalc = Simulator()

    def test_power_at_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.pcalc.power_at(1234)

    @patch('pvsim.simulators.Simulator.power_at', return_value=1234)
    def test_current_power_calls_power_at(self, power_at_mock):
        power, _ = self.pcalc.current_power()
        self.assertEqual(power, 1234)

    def test_get_angle(self):
        angle = self.pcalc.get_angle(45, 0, 360)
        self.assertAlmostEqual(angle, pi/4)

    @patch('pvsim.simulators.random.random', return_value=0.5)
    def test_random(self, random_mock):
        random_value = self.pcalc.random()
        self.assertEqual(random_value, 0.95)
        random_value = self.pcalc.random(1)
        self.assertEqual(random_value, 0.5)


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
