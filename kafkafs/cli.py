#!/usr/bin/env python

import logging

from threading import Thread

import click

from fuse import FUSE

from kafkafs.slave import Slave
from kafkafs.master import Master


@click.group()
def main():
    pass


@main.command()
@click.argument('root')
@click.option('--broker')
@click.option('--slaves', default=1,
              help="number of slave threads to run (shouldn't be greater than "
                   "count of topic partitions in kafka)")
def slave(root, broker, slaves):
    """Run KafkaFS slave"""
    for i in range(slaves):
        slave_thread = Thread(target=Slave().run)
        slave_thread.start()


@main.command()
@click.argument('root')
@click.argument('mountpoint')
@click.option('--broker')
@click.option('--foreground', is_flag=True)
@click.option('--slaves', default=1,
              help="number of slave threads to run (shouldn't be greater than "
                   "count of topic partitions in kafka)")
def master(root, mountpoint, foreground, broker, slaves):
    '''Mount a FUSE filesystem for KafkaFS master
    '''

    logging.basicConfig(level=logging.DEBUG)

    for i in range(slaves):
        slave_thread = Thread(target=Slave().run)
        slave_thread.start()

    FUSE(Master(root), mountpoint, foreground=foreground)

if __name__ == "__main__":
    main()
