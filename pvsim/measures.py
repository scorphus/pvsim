#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

from math import cos
from pvsim.base import PowerCalc


class Measure(object):

    def readout(self):
        raise NotImplementedError('readout should be implemented by subclass')


class HPCMeasure(Measure, PowerCalc):
    '''The HPCMeasure (Home Power Consumption) implements an average home
    consumption measure, simulated. It generates random but continuous values
    from 0 to 9000 Watts. For simplicity, it doesn't consider time of the year,
    latitude and longitude to determine how much the weather conditions and
    location would interfere in power consumption. Same applies to whether it's
    DST or not.

    :param max_power: maximum power consumption (in watt)
    :param breakfast_start: average time when the houses start waking up
    :param breakfast_end: average time when most houses are left alone
    :param lunch_start: average time when people begin having lunch
    :param lunch_end: average time when most people are done with lunch
    :param dinner_start: average time when people start coming back home
    :param dinner_end: average time when most people are in bed
    '''

    def __init__(
        self,
        max_power=9000,
        breakfast_start=5*3600,
        breakfast_end=9*3600,
        lunch_start=11*3600,
        lunch_end=13*3600,
        dinner_start=17*3600,
        dinner_end=24*3600,
    ):
        self.max_power = max_power
        self.breakfast_start = int(breakfast_start)
        self.breakfast_end = int(breakfast_end)
        self.breakfast = breakfast_end - breakfast_start  # breakfast duration
        self.lunch_start = int(lunch_start)
        self.lunch_end = int(lunch_end)
        self.lunch = lunch_end - lunch_start  # lunch duration
        self.dinner_start = int(dinner_start)
        self.dinner_end = int(dinner_end)
        self.dinner = dinner_end - dinner_start  # dinner duration
        self._validate()

    def _validate(self):
        if self.breakfast <= 0:
            raise ValueError('inappropriate values for breakfast start/end')
        if self.lunch <= 0:
            raise ValueError('inappropriate values for lunch start/end')
        if self.lunch_start < self.breakfast_end:
            raise ValueError('inappropriate value for lunch start')
        if self.dinner <= 0:
            raise ValueError('inappropriate values for dinner start/end')
        if self.dinner_start < self.lunch_end:
            raise ValueError('inappropriate value for dinner start')

    def _values_at_breakfast(self, seconds):
        step = 1000
        if seconds > self.breakfast_start + self.breakfast / 2:
            step = 1500
        max_power = self.max_power / 2.5 * self.random(8) - step
        angle = self.get_angle(seconds, self.breakfast_start, self.breakfast)
        return step, max_power, angle

    def _values_at_lunch(self, seconds):
        step = 1500
        max_power = self.max_power / 4 * self.random(6) - step
        angle = self.get_angle(seconds, self.lunch_start, self.lunch)
        return step, max_power, angle

    def _values_at_dinner(self, seconds):
        step = 1500
        if seconds > self.dinner_start + self.dinner / 2:
            step = 1000
        max_power = self.max_power * self.random() - step
        angle = self.get_angle(seconds, self.dinner_start, self.dinner)
        return step, max_power, angle

    def power_at(self, seconds):
        if seconds < self.breakfast_start:
            return 1000 * self.random(20)
        if seconds <= self.breakfast_end:
            step, max_power, angle = self._values_at_breakfast(seconds)
        elif (seconds < self.lunch_start or
              self.lunch_end < seconds < self.dinner_start):
            return 1500 * self.random(20)
        elif seconds <= self.lunch_end:
            step, max_power, angle = self._values_at_lunch(seconds)
        else:
            step, max_power, angle = self._values_at_dinner(seconds)
        return step + max_power * (1 - cos(angle)) / 2

    def daylight_range(self, step=50):
        return range(self.breakfast_start, self.sunset, step)

    def readout(self):
        return self.current_power()
