#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

import matplotlib.pyplot as plt
import random
import time

from math import cos, pi


class Simulator(object):

    #: The length of a day in seconds. For simplicity this doesn't take leap
    # seconds into account.
    day_length = 24 * 3600

    def current_power(self):
        localtime = time.localtime()
        seconds = (localtime.tm_hour * 3600 + localtime.tm_min * 60 +
                   localtime.tm_sec)
        return self.power_at(seconds), localtime

    def day_range(self, step=50):
        return range(0, self.day_length, step)

    def daylight_range(self, step):
        raise NotImplementedError(
            'daylight_range should be implemented by subclass'
        )

    def get_angle(self, seconds, start, duration):
        return 2 * (seconds - start) * pi / duration

    def power_at(self, seconds):
        raise NotImplementedError('power_at should be implemented by subclass')

    def random(self, factor=10):
        return (factor - random.random()) / factor


class PVSimulator(Simulator):
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
        self.light_hours = sunset - sunrise  # duration of daylight in seconds

    def power_at(self, seconds):
        if seconds < self.sunrise or seconds > self.sunset:
            return 0
        angle = self.get_angle(seconds, self.sunrise, self.light_hours)
        power = self.max_power * (1 - cos(angle)) / 2
        return power * self.random()

    def daylight_range(self, step=50):
        return range(self.sunrise, self.sunset, step)

    def plot_day(self):
        x = list(self.day_range(200))
        y = [self.power_at(xi) for xi in x]
        fig, ax = plt.subplots(1, 1)
        ax.plot(x, y, 'r-', lw=1, alpha=0.6, label='PVSimulator')
        plt.show()
