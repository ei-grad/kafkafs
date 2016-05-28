from uuid import getnode
import logging
import os

import six

from pykafka import KafkaClient
from pykafka.common import OffsetType

from kafkafs.fuse_pb2 import FuseChange


logger = logging.getLogger(__name__)


CREATE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_TRUNC


class Slave():

    def __init__(self, filemanager, broker, topic, futures=None,
                 fetch_max_wait_ms=10):
        self.fm = filemanager
        self.broker = broker
        self.topic = topic
        self.futures = {} if futures is None else futures
        self.fetch_max_wait_ms = fetch_max_wait_ms

    def run(self):
        self.client = KafkaClient(hosts=self.broker)
        topic = self.client.topics[self.topic]
        consumer_group = six.b('%s:%s' % (getnode(), self.fm.root))
        consumer = topic.get_simple_consumer(
            consumer_group,
            use_rdkafka=True,
            auto_offset_reset=OffsetType.LATEST,
        )
        logger.info("Started kafkafs slave on %s", self.fm.root)
        for kafka_msg in consumer:
            msg = FuseChange.FromString(kafka_msg.value)
            logger.debug("%s", msg)
            ret = getattr(self, FuseChange.Operation.Name(msg.op))(msg)
            if msg.uuid in self.futures:
                self.futures[msg.uuid].set_result(ret)

    def p(self, path):
        return self.fm.p(path)

    def CHMOD(self, msg):
        return os.chmod(self.p(msg.path), msg.mode)

    def CHOWN(self, msg):
        return os.chown(self.p(msg.path), msg.uid, msg.gid)

    def CREATE(self, msg):
        return self.fm.open(msg.uuid, msg.path, CREATE_FLAGS, msg.mode)

    def FLUSH(self, msg):
        return os.fsync(self.fm[msg.fh_uuid].fh)

    def FSYNC(self, msg):
        fh = self.fm[msg.fh_uuid].fh
        if msg.datasync:
            return os.fdatasync(fh)
        else:
            return os.fsync(fh)

    def LINK(self, msg):
        return os.link(self.p(msg.src), self.p(msg.path))

    def MKDIR(self, msg):
        return os.mkdir(self.p(msg.path), msg.mode)

    def OPEN(self, msg):
        return self.fm.open(msg.uuid, msg.path, msg.flags, msg.mode)

    def RELEASE(self, msg):
        fh = self.fm[msg.fh_uuid].fh
        del self.fm[msg.fh_uuid]
        return os.close(fh)

    def RMDIR(self, msg):
        return os.rmdir(self.p(msg.path))

    def SYMLINK(self, msg):
        return os.symlink(msg.src, self.p(msg.path))

    def TRUNCATE(self, msg):
        with open(self.p(msg.path), 'r+') as f:
            return f.truncate(msg.length)

    def UNLINK(self, msg):
        return os.unlink(self.p(msg.path))

    def UTIME(self, msg):
        return os.utime(self.p(msg.path), (msg.atime, msg.mtime))

    def WRITE(self, msg):
        filehandle = self.fm[msg.fh_uuid]
        with filehandle.lock:
            os.lseek(filehandle.fh, msg.offset, 0)
            # XXX: what if returned less than len(msg.data)??
            return os.write(filehandle.fh, msg.data)
