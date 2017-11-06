#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

import json
import logging
import time


class GenericMeter(object):

    def __init__(self, measure, broker, interval=2):
        self.measure = measure
        self.broker = broker
        self.interval = interval

    def publish(self):
        power, localtime = self.measure.readout()
        data = {
            'localtime': localtime,
            'power': power,
        }
        if self.broker.publish(json.dumps(data)):
            logging.info('[GenericMeter] Sent %s', data)

    def publish_periodically(self):
        while True:
            self.publish()
            try:
                time.sleep(self.interval)
            except KeyboardInterrupt:
                logging.info('[GenericMeter] Stoping...')
                return
