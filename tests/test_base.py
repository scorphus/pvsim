#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

from math import pi
from mock import patch
from pvsim.base import PowerCalc
from unittest import TestCase


class PowerCalcTestCase(TestCase):

    def setUp(self):
        self.pcalc = PowerCalc()

    def test_power_at_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.pcalc.power_at(1234)

    @patch('pvsim.simulators.PowerCalc.power_at', return_value=1234)
    def test_current_power_and_time_calls_power_at(self, power_at_mock):
        power, localtime = self.pcalc.current_power_and_time()
        self.assertEqual(power, 1234)
        power_at_mock.assert_called_once_with(
            localtime.tm_hour * 3600 + localtime.tm_min * 60 + localtime.tm_sec
        )

    def test_get_angle(self):
        angle = self.pcalc.get_angle(45, 0, 360)
        self.assertAlmostEqual(angle, pi/4)

    @patch('pvsim.base.random.random', return_value=0.5)
    def test_random(self, random_mock):
        random_value = self.pcalc.random()
        self.assertEqual(random_value, 0.95)
        random_value = self.pcalc.random(1)
        self.assertEqual(random_value, 0.5)
