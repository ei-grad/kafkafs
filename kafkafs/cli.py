#!/usr/bin/env python

import logging

from threading import Thread

import click

from fuse import FUSE

from pykafka import KafkaClient
from pykafka.common import CompressionType

from kafkafs.slave import Slave
from kafkafs.master import Master
from kafkafs.filemanager import FileManager


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
@click.option('--fetch-wait-max-ms', default=10)
def slave(root, topic, broker, slaves, fetch_wait_max_ms):
    """Run KafkaFS slave"""

    topic = topic.encode('ascii')

    fm = FileManager(root)

    def get_slave():
        return Slave(
            fm, broker, topic,
            fetch_max_wait_ms=fetch_wait_max_ms
        )

    if slaves > 1:

        slaves = [
            Thread(target=get_slave().run)
            for i in range(slaves)
        ]

        for thread in slaves:
            thread.start()

        for thread in slaves:
            thread.join()

    else:
        get_slave().run()


@main.command()
@click.argument('root')
@click.argument('topic')
@click.argument('mountpoint')
@opt_broker
@opt_slaves
@click.option('--foreground', is_flag=True)
@click.option('--linger-ms', default=10)
@click.option('--max-write', default=900000)
def master(root, topic, mountpoint, foreground, broker, slaves,
           linger_ms, max_write):
    '''Mount a FUSE filesystem for KafkaFS master'''

    futures = {}
    fm = FileManager(root)

    for i in range(slaves):
        slave_thread = Thread(target=Slave(
            fm, broker, topic.encode('ascii'),
            futures, fetch_max_wait_ms=linger_ms,
        ).run)
        slave_thread.start()

    kafka = KafkaClient(hosts=broker)
    producer = kafka.topics[topic.encode('ascii')].get_producer(
        use_rdkafka=True,
        compression=CompressionType.SNAPPY,
        linger_ms=linger_ms,
    )
    master = Master(fm, producer, futures, max_bytes=max_write)

    FUSE(master, mountpoint, foreground=foreground,
         big_writes=True, max_write=max_write,
         fsname='kafkafs://{}/{}'.format(broker, topic))


if __name__ == "__main__":
    main()
