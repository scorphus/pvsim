#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of pvsim.
# https://github.com/scorphus/pvism

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, Pablo Santiago Blum de Aguiar <pablo.aguiar@gmail.com>

import logging
import sys
import toml

from pvsim import __version__
from pvsim.argparser import ArgParser


def import_class(import_path):
    path_parts = import_path.split('.')
    module_path, class_ = '.'.join(path_parts[:-1]), path_parts[-1]
    module = __import__(module_path)
    return getattr(module, class_)


def instantiate_component(component, config, **init_kwargs):
    component_config = config.get(component)
    if not component_config or not component_config.get('class'):
        logging.error(
            '[main] Could not intantiate a %s: no class specified in config',
            component,
        )
        sys.exit(1)
    component_class = import_class(component_config.get('class'))
    parameters = component_config.get('parameters', {})
    parameters.update(init_kwargs)
    return component_class(**parameters)


def load_config(config_file):
    try:
        return toml.load(config_file)
    except Exception as e:
        logging.error('[main] Could not load config: %s', e)
        sys.exit(1)


def run_meter(config):
    measure = instantiate_component('measure', config)
    broker = instantiate_component('broker', config)
    meter = instantiate_component(
        'meter', config, measure=measure, broker=broker
    )
    logging.info('Starting meter...')
    meter.publish_periodically()
    logging.info('Meter stopped')
    broker.disconnect()


def run_simulator(config):
    simulator = instantiate_component('simulator', config)
    writer = instantiate_component('writer', config)
    simulator.set_writer(writer)
    logging.info('Starting simulator...')
    broker = instantiate_component('broker', config)
    simulator.consume_from_broker(broker)
    logging.info('Simulator stopped')
    broker.disconnect()


def set_log_level(parsed_args):
    logger = logging.getLogger()
    if parsed_args.verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)


def main():
    parser = ArgParser()
    parsed_args = parser.parse()
    set_log_level(parsed_args)
    if parsed_args.help:
        parser.print_help()
    elif parsed_args.version:
        parser.print_version(__version__)
    elif parsed_args.action:
        config = load_config(parsed_args.config)
        if parsed_args.action == 'meter':
            run_meter(config)
        elif parsed_args.action == 'simulator':
            run_simulator(config)
        elif parsed_args.action == 'plot':
            logging.error('Not implemented yet, sorry')
        else:
            logging.error('No such action: %s', parsed_args.action)
            parser.print_usage()
    else:
        parser.print_usage()
