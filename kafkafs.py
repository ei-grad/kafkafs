#!/usr/bin/env python
from __future__ import print_function, absolute_import, division

import logging

from errno import EACCES
from os.path import realpath
from threading import Thread, Lock
from concurrent.futures import Future
from uuid import getnode, uuid1

import os

import click

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn, ENOTSUP
from pykafka import KafkaClient
from pykafka.common import CompressionType

from fuse_pb2 import FuseChange


class Slave():

    def __init__(self, root, broker, topic, futures=None):
        self.root = realpath(root)
        self.broker = broker
        self.topic = topic
        self.futures = futures

    def run(self):
        topic = KafkaClient(hosts=self.broker).topics[self.topic]
        consumer_group = '%s:%s' % (getnode(), self.root)
        consumer = topic.get_balanced_consumer(
            consumer_group,
            managed=True,
            use_rdkafka=True,
        )
        for msg in consumer:
            print(msg)


class Sequence():

    def __init__(self, start=0, delta=1):
        self.lock = Lock()
        self.value = start - delta
        self.delta = delta

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            self.value += self.delta
            return self.value


class Master(LoggingMixIn, Operations):
    def __init__(self, root, broker, topic):
        self.root = realpath(root)
        self.producer = KafkaClient(hosts=broker).topics[topic].get_producer(
            use_rdkafka=True, compression=CompressionType.SNAPPY
        )
        self._uuid_seq = Sequence()
        self._node = getnode()

    def _send(self, kwargs):
        if 'uuid' not in kwargs:
            kwargs['uuid'] = self._get_uuid()
        return self.producer.produce(FuseChange(**kwargs).SerializeToString())

    def _get_uuid(self):
        return uuid1(node=self._node, clock_seq=next(self._uuid_seq))

    def access(self, path, mode):
        if not os.access(self.root + path, mode):
            raise FuseOSError(EACCES)

    def chmod(self, path, mode):
        self._send(FuseChange(
            op=FuseChange.CHMOD
        ))
        return os.chmod(path, mode)

    def chown(self, path, uid, gid):
        return os.chown(path, uid, gid)

    def create(self, path, mode):
        return os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, mode)

    def flush(self, path, fh):
        return os.fsync(fh)

    def fsync(self, path, datasync, fh):
        if datasync != 0:
            return os.fdatasync(fh)
        else:
            return os.fsync(fh)

    def getattr(self, path, fh=None):
        st = os.lstat(path)
        return dict((key, getattr(st, key)) for key in (
            'st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime',
            'st_nlink', 'st_size', 'st_uid'
        ))

    def link(self, target, source):
        return os.link(source, target)

    def mkdir(self, path, mode):
        return os.mkdir(path, mode)

    def mknod(self, *args):
        raise FuseOSError(ENOTSUP)

    def open(self, path, flags):
        uuid = self._get_uuid().bytes
        future = Future()
        self.futures[uuid] = future
        self._send(FuseChange(
            uuid=uuid,
            op=FuseChange.OPEN,
            path=path,
            flags=self._get_flags(flags),
        ))
        fh = future.result()
        self.locks[fh] = Lock()
        return fh

    def read(self, path, size, offset, fh):
        with self.locks[fh]:
            os.lseek(fh, offset, 0)
            return os.read(fh, size)

    def readdir(self, path, fh):
        return ['.', '..'] + os.listdir(path)

    readlink = os.readlink

    def release(self, path, fh):
        del self.locks[fh]
        return os.close(fh)

    def rename(self, old, new):
        # XXX: not idempotent! should be unlink/write[] ??
        return os.rename(old, self.root + new)

    rmdir = os.rmdir

    def statfs(self, path):
        stv = os.statvfs(path)
        return dict((key, getattr(stv, key)) for key in (
            'f_bavail', 'f_bfree', 'f_blocks', 'f_bsize', 'f_favail',
            'f_ffree', 'f_files', 'f_flag', 'f_frsize', 'f_namemax'
        ))

    def symlink(self, target, source):
        return os.symlink(source, target)

    def truncate(self, path, length, fh=None):
        with open(path, 'r+') as f:
            f.truncate(length)

    unlink = os.unlink
    utimens = os.utime

    def write(self, path, data, offset, fh):
        with self.rwlock:
            os.lseek(fh, offset, 0)
            return os.write(fh, data)


@click.group()
def main():
    pass


@main.command()
def slave():
    """Run KafkaFS slave"""
    Slave().run()


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
