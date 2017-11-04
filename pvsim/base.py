#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

import random
import time

from math import pi


class PowerCalc(object):

    #: The length of a day in seconds. For simplicity, this doesn't take leap
    # seconds into account.
    day_length = 24 * 3600

    def current_power(self):
        localtime = time.localtime()
        seconds = (localtime.tm_hour * 3600 + localtime.tm_min * 60 +
                   localtime.tm_sec)
        return self.power_at(seconds), localtime

    def day_range(self, step):
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
