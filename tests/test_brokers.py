#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

from mock import MagicMock, patch
from pika.exceptions import ConnectionClosed
from pvsim.brokers import RabbitMQBroker, Broker
from unittest import TestCase


class BrokerTestCase(TestCase):

    def setUp(self):
        self.broker = Broker()

    def test_connect_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.broker.connect()

    def test_disconnect_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.broker.disconnect()

    def test_publish_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.broker.publish('...')


class RabbitMQBrokerInitTestCase(TestCase):

    @patch('pvsim.brokers.RabbitMQBroker.connect')
    def test_init_calls_connect(self, connect_mock):
        RabbitMQBroker('localhost', 5672, 'exchange', 'key')
        connect_mock.assert_called_once()


class RabbitMQBrokerTestCase(TestCase):

    def setUpConnectionParametersPatcher(self):
        self.params = MagicMock(host='localhost', port=5672)
        self.cp_patcher = patch('pvsim.brokers.pika.ConnectionParameters')
        self.cp_mock = self.cp_patcher.start()
        self.cp_mock.return_value = self.params

    def setUpBlockingConnectionPatcher(self):
        self.connection = MagicMock(is_closed=False)
        self.bc_patcher = patch('pvsim.brokers.pika.BlockingConnection')
        self.bc_mock = self.bc_patcher.start()
        self.bc_mock.return_value = self.connection

    def setUp(self):
        self.setUpConnectionParametersPatcher()
        self.setUpBlockingConnectionPatcher()
        self.broker = RabbitMQBroker('localhost', 5672, 'exchange', 'key')

    def tearDown(self):
        self.bc_patcher.stop()
        self.cp_patcher.stop()

    def test_connect_connects_to_broker(self):
        self.cp_mock.assert_called_once_with(host='localhost', port=5672)
        self.bc_mock.assert_called_once_with(self.params)
        self.broker.channel.exchange_declare.assert_called_once_with(
            exchange='exchange', exchange_type='direct'
        )

    def test_publish_publishes_to_broker(self):
        self.broker.publish('body')
        self.broker.channel.basic_publish.assert_called_once_with(
            exchange='exchange', routing_key='key', body='body'
        )

    @patch('pvsim.brokers.logging')
    @patch('pvsim.brokers.pika.BlockingConnection')
    def test_connect_errs_upon_exception(self, bc_mock, log_mock):
        bc_mock.side_effect = ConnectionClosed('Connection refused')
        self.broker.connect()
        self.assertEqual(self.cp_mock.call_count, 2)
        bc_mock.assert_called_once_with(self.params)
        self.bc_mock.assert_called_once()
        log_mock.error.assert_called_once()
        self.assertIsNone(self.broker.connection)
        self.assertIsNone(self.broker.channel)
