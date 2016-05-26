from os.path import realpath
from uuid import getnode
import logging
import os

import six

from pykafka import KafkaClient

from kafkafs.fuse_pb2 import FuseChange
from kafkafs.utils import FileHandle, flags_os2pbf, flags_pbf2os


logger = logging.getLogger(__name__)


class Slave():

    def __init__(self, root, broker, topic, futures=None, files=None):
        self.root = realpath(root)
        self.broker = broker
        self.topic = topic
        self.futures = {} if futures is None else futures
        self.files = {} if files is None else files

    def run(self):
        self.client = KafkaClient(hosts=self.broker)
        topic = self.client.topics[self.topic]
        consumer_group = six.b('%s:%s' % (getnode(), self.root))
        consumer = topic.get_balanced_consumer(
            consumer_group,
            use_rdkafka=True,
        )
        logger.info("Started kafkafs slave on %s", self.root)
        for kafka_msg in consumer:
            msg = FuseChange.FromString(kafka_msg.value)
            logger.debug("%s", msg)
            ret = getattr(self, FuseChange.Operation.Name(msg.op))(msg)
            if msg.uuid in self.futures:
                self.futures[msg.uuid].set_result(ret)

    def p(self, path):
        assert path[0] == '/'
        ret = os.path.join(self.root, path[1:])
        assert realpath(ret).startswith(self.root)
        return ret

    def CHMOD(self, msg):
        return os.chmod(self.p(msg.path), msg.mode)

    def CHOWN(self, msg):
        return os.chown(self.p(msg.path), msg.uid, msg.gid)

    def CREATE(self, msg):
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        fh = os.open(self.p(msg.path), flags, msg.mode)
        filehandle = FileHandle(
            path=msg.path,
            uuid=msg.uuid,
            flags=flags_os2pbf(flags),
            fh=fh,
        )
        self.files[msg.uuid] = filehandle
        return filehandle

    def FLUSH(self, msg):
        return os.fsync(self.files[msg.fh_uuid].fh)

    def FSYNC(self, msg):
        fh = self.files[msg.fh_uuid].fh
        if msg.datasync:
            return os.fdatasync(fh)
        else:
            return os.fsync(fh)

    def LINK(self, msg):
        return os.link(self.p(msg.src), self.p(msg.path))

    def MKDIR(self, msg):
        return os.mkdir(self.p(msg.path), msg.mode)

    def OPEN(self, msg):
        fh = os.open(self.p(msg.path), flags_pbf2os(msg.flags), msg.mode)
        filehandle = FileHandle(
            path=msg.path,
            uuid=msg.uuid,
            flags=msg.flags,
            fh=fh,
        )
        self.files[msg.uuid] = filehandle
        return filehandle

    def RELEASE(self, msg):
        fh = self.files[msg.fh_uuid].fh
        del self.files[msg.fh_uuid]
        return os.close(fh)

    def SYMLINK(self, msg):
        return os.symlink(self.p(msg.src), self.p(msg.path))

    def TRUNCATE(self, msg):
        with open(self.p(msg.path), 'r+') as f:
            return f.truncate(msg.length)

    def UNLINK(self, msg):
        return os.unlink(self.p(msg.path))

    def WRITE(self, msg):
        filehandle = self.files[msg.fh_uuid]
        with filehandle.lock:
            os.lseek(filehandle.fh, msg.offset, 0)
            # XXX: what if returned less than len(msg.data)??
            return os.write(filehandle.fh, msg.data)
