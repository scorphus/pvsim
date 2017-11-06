#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

import logging
import pika


class Broker(object):

    def connect(self):
        raise NotImplementedError('connect should be implemented by subclass')

    def disconnect(self):
        raise NotImplementedError(
            'disconnect should be implemented by subclass'
        )

    def publish(self, body):
        raise NotImplementedError('publish should be implemented by subclass')

    def start_consuming(self, callback):
        raise NotImplementedError(
            'start_consuming should be implemented by subclass'
        )


class RabbitMQBroker(Broker):

    def __init__(self, host, port, exchange, routing_key):
        self.host = host
        self.port = port
        self.exchange = exchange
        self.routing_key = routing_key
        self.connect()

    def connect(self):
        params = pika.ConnectionParameters(host=self.host, port=self.port)
        try:
            self.connection = pika.BlockingConnection(params)
        except pika.exceptions.ConnectionClosed as e:
            self.connection, self.channel = None, None
            logging.error(
                '[RabbitMQBroker] Unable to connect to RabbitMQ server: %s', e
            )
            return
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.exchange, exchange_type='direct'
        )

    def disconnect(self):
        if self.connection is not None and not self.connection.is_closed:
            self.connection.close()

    def publish(self, body):
        if self.connection is None or self.channel is None:
            self.connect()
        if self.connection is not None and not self.connection.is_closed:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=body,
            )
            return True
        return False

    def start_consuming(self, callback):
        if self.connection is None or self.channel is None:
            self.connect()
        if self.connection is not None and not self.connection.is_closed:
            result = self.channel.queue_declare(exclusive=True)
            queue = result.method.queue
            self.channel.queue_bind(
                exchange=self.exchange,
                queue=queue,
                routing_key=self.routing_key,
            )
            self.channel.basic_consume(callback, queue=queue, no_ack=True)
            self.channel.start_consuming()
