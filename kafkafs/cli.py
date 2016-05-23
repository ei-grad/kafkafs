#!/usr/bin/env python

import logging

from threading import Thread

import click

from fuse import FUSE

from kafkafs.slave import Slave
from kafkafs.master import Master


@click.group()
@click.option('--debug', is_flag=True)
def main(debug):
    logging.basicConfig(level='DEBUG' if debug else 'INFO')


opt_slaves = click.option(
    '--slaves', default=1,
    help="number of slave threads to run (shouldn't be greater than count of "
         "topic partitions in kafka)"
)

opt_broker = click.option('--broker', default='localhost:9092')


@main.command()
@click.argument('root')
@click.argument('topic')
@opt_broker
@opt_slaves
def slave(root, topic, broker, slaves):
    """Run KafkaFS slave"""
    if slaves > 1:
        for i in range(slaves):
            slave_thread = Thread(target=Slave(root, broker, topic).run)
            slave_thread.start()
    else:
        Slave(root, broker, topic).run()


@main.command()
@click.argument('root')
@click.argument('topic')
@click.argument('mountpoint')
@opt_broker
@opt_slaves
@click.option('--foreground', is_flag=True)
def master(root, topic, mountpoint, debug, foreground, broker, slaves):
    '''Mount a FUSE filesystem for KafkaFS master
    '''

    for i in range(slaves):
        slave_thread = Thread(target=Slave(root, broker, topic).run)
        slave_thread.start()

    FUSE(Master(root, broker, topic), mountpoint, foreground=foreground)


if __name__ == "__main__":
    main()
