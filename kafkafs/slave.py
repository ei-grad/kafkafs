from os.path import realpath
from uuid import getnode
import os

from pykafka import KafkaClient

from kafkafs.fuse_pb2 import FuseChange
from kafkafs.utils import FileHandle


class Slave():

    def __init__(self, root, broker, topic, futures=None, files=None):
        self.root = realpath(root)
        self.broker = broker
        self.topic = topic
        self.futures = futures
        if files is None:
            files = {}
        self.files = files

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
            print(FuseChange)

    def p(self, path):
        return os.path.join(self.root, path)

    def chmod(self, msg):
        return os.chmod(self.p(msg.path), msg.mode)

    def chown(self, msg):
        return os.chown(self.p(msg.path), msg.uid, msg.gid)

    def create(self, msg):
        return os.open(self.p(msg.path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, msg.mode)

    def flush(self, msg):
        return os.fsync(self.files[msg.fh_uuid].fh)

    def fsync(self, msg):
        fh = self.files[msg.fh_uuid].fh
        if msg.datasync:
            return os.fdatasync(fh)
        else:
            return os.fsync(fh)

    def link(self, msg):
        return os.link(self.p(msg.src), self.p(msg.path))

    def mkdir(self, msg):
        return os.mkdir(self.p(msg.path), msg.mode)

    def open(self, msg):
        fh = os.open(self.p(msg.path), self.flags(msg.flags), msg.mode)
        filehandle = FileHandle(
            path=msg.path,
            uuid=msg.uuid,
            flags=msg.flags,
            mode=msg.mode,
            fh=fh,
        )
        self.files[msg.uuid] = filehandle
        return filehandle

    def symlink(self, msg):
        return os.symlink(self.p(msg.src), self.p(msg.path))

    def truncate(self, msg):
        with open(self.p(msg.path), 'r+') as f:
            return f.truncate(msg.length)

    def unlink(self, msg):
        return os.unlink(self.p(msg.path))

    def write(self, msg):
        filehandle = self.files[msg.fh_uuid]
        with filehandle.lock:
            os.lseek(filehandle.fh, msg.offset, 0)
            # XXX: what if returned less than len(msg.data)??
            return os.write(filehandle.fh, msg.data)
