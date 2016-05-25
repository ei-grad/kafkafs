#!/usr/bin/env python

import logging

from threading import Thread

import click

from fuse import FUSE

from pykafka import KafkaClient
from pykafka.common import CompressionType

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

    topic = topic.encode('ascii')

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
@click.option('--linger-ms', default=10)
def master(root, topic, mountpoint, foreground, broker, slaves, linger_ms):
    '''Mount a FUSE filesystem for KafkaFS master'''

    futures = {}
    files = {}

    for i in range(slaves):
        slave_thread = Thread(target=Slave(
            root, broker, topic.encode('ascii'),
            futures, files
        ).run)
        slave_thread.start()

    kafka = KafkaClient(hosts=broker)
    producer = kafka.topics[topic.encode('ascii')].get_producer(
        use_rdkafka=True,
        compression=CompressionType.SNAPPY,
        linger_ms=linger_ms,
    )
    master = Master(root, producer, futures, files)
    FUSE(master, mountpoint, foreground=foreground,
         fsname='kafkafs://{}/{}'.format(broker, topic))


if __name__ == "__main__":
    main()
