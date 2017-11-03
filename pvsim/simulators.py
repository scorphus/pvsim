#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

from math import cos
from pvsim.base import PowerCalc


class PVSimulator(PowerCalc):
    '''The PVSimulator simulates a photovoltaic power generator. For simplicity,
    it doesn't consider time of the year nor latitude to determine how much
    weather conditions and location would interfere in power generation.

    :param max_power: maximum power this PV system can generate (in Watt)
    :param sunrise: time of sunrise in seconds since the beginning of the day
    :param sunset: time of sunset in seconds since the beginning of the day
    '''

    def __init__(self, max_power=3300, sunrise=6*3600, sunset=20.5*3600):
        self.max_power = max_power
        self.sunrise = int(sunrise)
        self.sunset = int(sunset)
        if sunset <= sunrise:
            raise ValueError('inappropriate values for sunrise and sunset')
        self.light_hours = sunset - sunrise  # duration of daylight in seconds

    def power_at(self, seconds):
        if seconds < self.sunrise or seconds > self.sunset:
            return 0
        angle = self.get_angle(seconds, self.sunrise, self.light_hours)
        power = self.max_power * (1 - cos(angle)) / 2
        return power * self.random()

    def daylight_range(self, step=50):
        return range(self.sunrise, self.sunset, step)
