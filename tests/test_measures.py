#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

import pytest

from math import pi
from mock import patch
from pvsim.measures import HPCMeasure, Measure
from unittest import TestCase


@pytest.mark.parametrize(('bf_start, bf_end, lunch_start, lunch_end, '
                          'dinner_start, dinner_end, member'), [
    (123, 123, 123, 123, 123, 123, 'inappropriate values for breakfast'),
    (123, 124, 124, 124, 124, 124, 'inappropriate values for lunch'),
    (123, 124, 124, 125, 125, 125, 'inappropriate values for dinner'),
    (123, 124, 123, 124, 124, 124, 'inappropriate value for lunch'),
    (123, 124, 124, 125, 124, 125, 'inappropriate value for dinner'),
    (123, 'a', 124, 125, 125, 126, 'invalid literal'),
])
def test_hpc_measure_init_raises_value_error(
    bf_start,
    bf_end,
    lunch_start,
    lunch_end,
    dinner_start,
    dinner_end,
    member,
):
    with pytest.raises(ValueError) as e:
        HPCMeasure(
            1234,
            bf_start,
            bf_end,
            lunch_start,
            lunch_end,
            dinner_start,
            dinner_end,
        )
    assert member in e.value.args[0]


class MeasureTestCase(TestCase):

    def test_readout_raises_not_implemented(self):
        self.measure = Measure()
        with self.assertRaises(NotImplementedError):
            self.measure.readout()


class HPCMeasureTestCase(TestCase):

    def setUp(self):
        self.hpcm = HPCMeasure()
        self.patcher = patch('pvsim.measures.HPCMeasure.random', return_value=1)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_power_at_returns_lower_if_before_breackfast(self):
        two_am = 2 * 3600
        power = self.hpcm.power_at(two_am)
        self.assertEqual(power, 1000)

    def test_power_at_returns_low_when_past_breakfast(self):
        ten_am = 10 * 3600
        power = self.hpcm.power_at(ten_am)
        self.assertEqual(power, 1500)

    def test_power_at_returns_low_when_past_lunch(self):
        three_pm = 15 * 3600
        power = self.hpcm.power_at(three_pm)
        self.assertEqual(power, 1500)

    def test_power_at_increases_when_into_breakfast(self):
        seconds_a = 6 * 3600
        power_a = self.hpcm.power_at(seconds_a)
        seconds_b = 7 * 3600
        power_b = self.hpcm.power_at(seconds_b)
        self.assertGreater(power_b, power_a)
        self.assertGreater(power_a, 1000)

    def test_power_at_decreases_when_out_from_breakfast(self):
        seconds_a = 7 * 3600
        power_a = self.hpcm.power_at(seconds_a)
        seconds_b = 8 * 3600
        power_b = self.hpcm.power_at(seconds_b)
        self.assertGreater(power_b, 1500)
        self.assertGreater(power_a, power_b)

    def test_power_at_increases_when_into_lunch(self):
        seconds_a = 11.5 * 3600
        power_a = self.hpcm.power_at(seconds_a)
        seconds_b = 12 * 3600
        power_b = self.hpcm.power_at(seconds_b)
        self.assertGreater(power_b, power_a)
        self.assertGreater(power_a, 1500)

    def test_power_at_decreases_when_out_from_lunch(self):
        seconds_a = 12 * 3600
        power_a = self.hpcm.power_at(seconds_a)
        seconds_b = 12.5 * 3600
        power_b = self.hpcm.power_at(seconds_b)
        self.assertGreater(power_b, 1500)
        self.assertGreater(power_a, power_b)

    def test_power_at_increases_when_into_dinner(self):
        seconds_a = 18 * 3600
        power_a = self.hpcm.power_at(seconds_a)
        seconds_b = 20.5 * 3600
        power_b = self.hpcm.power_at(seconds_b)
        self.assertGreater(power_b, power_a)
        self.assertGreater(power_a, 1500)

    def test_power_at_decreases_when_out_from_dinner(self):
        seconds_a = 20.5 * 3600
        power_a = self.hpcm.power_at(seconds_a)
        seconds_b = 23 * 3600
        power_b = self.hpcm.power_at(seconds_b)
        self.assertGreater(power_b, 1000)
        self.assertGreater(power_a, power_b)

    @patch('pvsim.measures.HPCMeasure.power_at', return_value=1234)
    def test_readout_calls_power_at(self, power_at_mock):
        power, localtime = self.hpcm.readout()
        self.assertEqual(power, 1234)
        power_at_mock.assert_called_once_with(
            localtime.tm_hour * 3600 + localtime.tm_min * 60 + localtime.tm_sec
        )
