#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

import json

from mock import MagicMock, patch
from pvsim.simulators import PVSimulator
from unittest import TestCase


class PVSimulatorTestCase(TestCase):

    def setUp(self):
        self.pvs = PVSimulator()

    def test_init_raises_value_error(self):
        with self.assertRaises(ValueError) as e:
            PVSimulator(1234, 0, 0)
        self.assertIn('inappropriate values', e.exception.args[0])
        with self.assertRaises(ValueError) as e:
            PVSimulator(1234, 'a', 4321)
        self.assertIn('invalid literal', e.exception.args[0])

    def test_power_at_returns_zero_if_before_sunrise(self):
        two_am = 2 * 3600
        power = self.pvs.power_at(two_am)
        self.assertEqual(power, 0)

    def test_power_at_returns_zero_when_past_sunset(self):
        eleven_pm = 23 * 3600
        power = self.pvs.power_at(eleven_pm)
        self.assertEqual(power, 0)

    def test_power_at_returns_gt_zero_when_light(self):
        noon = 12 * 3600
        power = self.pvs.power_at(noon)
        self.assertGreater(power, 0)

    def test_consume_from_broker_starts_comsuming(self):
        broker = MagicMock()
        self.pvs.consume_from_broker(broker)
        broker.start_consuming.assert_called_once()

    def test_message_received_writes_to_writer(self):
        data = {'localtime': '2017-11-06', 'power': 1234}
        writer = MagicMock()
        self.pvs.set_writer(writer)
        self.pvs.message_received(json.dumps(data))
        writer.write.assert_called_once()

    @patch('pvsim.simulators.logging.error')
    def test_message_received_errs_on_decode_error(self, error_mock):
        writer = MagicMock()
        self.pvs.set_writer(writer)
        self.pvs.message_received('unpackable')
        self.assertEqual(writer.write.call_count, 0)
        self.assertIn('Could not unpack message', error_mock.call_args[0][0])

    @patch('pvsim.simulators.logging.error')
    def test_message_received_errs_on_another_decode_error(self, error_mock):
        writer = MagicMock()
        self.pvs.set_writer(writer)
        self.pvs.message_received('{"a":2')
        self.assertEqual(writer.write.call_count, 0)
        self.assertIn('Could not unpack message', error_mock.call_args[0][0])

    @patch('pvsim.simulators.logging.error')
    def test_message_received_errs_on_key_error(self, error_mock):
        data = {'foo': 'bar', 'n': 359}
        writer = MagicMock()
        self.pvs.set_writer(writer)
        self.pvs.message_received(json.dumps(data))
        self.assertEqual(writer.write.call_count, 0)
        self.assertIn('Message is incomplete', error_mock.call_args[0][0])

    @patch('pvsim.simulators.logging.error')
    def test_message_received_errs_on_type_error(self, error_mock):
        data = {'localtime': '2017-11-06', 'power': '1234'}
        writer = MagicMock()
        self.pvs.set_writer(writer)
        self.pvs.message_received(json.dumps(data))
        self.assertEqual(writer.write.call_count, 0)
        self.assertIn('Message is incompatible', error_mock.call_args[0][0])
