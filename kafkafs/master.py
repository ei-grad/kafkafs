from concurrent.futures import Future
from errno import EACCES
from os.path import realpath
from uuid import getnode, uuid1
import os

from fuse import FuseOSError, Operations, LoggingMixIn, ENOTSUP

from kafkafs.fuse_pb2 import FuseChange
from kafkafs.utils import Sequence, flags_os2pbf


class Master(LoggingMixIn, Operations):
    def __init__(self, root, producer, futures, files):
        self.root = realpath(root)
        self.producer = producer
        self.futures = futures
        self.files = files

        self._uuid_seq = Sequence()
        self.node = getnode()

    def p(self, path):
        assert path[0] == '/'
        ret = os.path.join(self.root, path[1:])
        assert realpath(ret).startswith(self.root)
        return ret

    def send(self, **kwargs):
        return self.producer.produce(FuseChange(**kwargs).SerializeToString())

    def from_slave(self, **kwargs):
        if 'uuid' not in kwargs:
            kwargs['uuid'] = self.get_uuid().bytes
        future = Future()
        self.futures[kwargs['uuid']] = future
        self.send(**kwargs)
        return future.result()

    def get_uuid(self):
        return uuid1(node=self.node, clock_seq=next(self._uuid_seq))

    def access(self, path, mode):
        if not os.access(self.root + path, mode):
            raise FuseOSError(EACCES)

    def chmod(self, path, mode):
        return self.from_slave(op=FuseChange.CHMOD, path=path, mode=mode)

    def chown(self, path, uid, gid):
        return self.from_slave(op=FuseChange.CHOWN, path=path, uid=uid, gid=gid)

    def create(self, path, mode):
        return self.from_slave(op=FuseChange.CREATE, path=path, mode=mode)

    def flush(self, path, fh):
        return self.from_slave(op=FuseChange.FLUSH, path=path,
                               fh_uuid=self.files[fh].uuid)

    def fsync(self, path, datasync, fh):
        return self.from_slave(
            op=FuseChange.FSYNC,
            path=path,
            fh_uuid=self.files[fh].uuid,
            datasync=(datasync != 0),
        )

    def getattr(self, path, fh=None):
        st = os.lstat(self.root + path)
        return dict((key, getattr(st, key)) for key in (
            'st_atime', 'st_ctime', 'st_gid', 'st_mode', 'st_mtime',
            'st_nlink', 'st_size', 'st_uid'
        ))

    def link(self, path, src):
        return self.from_slave(op=FuseChange.LINK, path=path, src=src)

    def mkdir(self, path, mode):
        return self.from_slave(op=FuseChange.MKDIR, path=path, mode=mode)

    def mknod(self, *args):
        raise FuseOSError(ENOTSUP)

    def open(self, path, flags, mode=None):
        filehandle = self.from_slave(
            op=FuseChange.OPEN,
            path=path,
            flags=flags_os2pbf(flags),
            mode=mode,
        )
        self.files[filehandle.fh] = filehandle
        return filehandle.fh

    def read(self, path, size, offset, fh):
        with self.files[fh].lock:
            os.lseek(fh, offset, 0)
            return os.read(fh, size)

    def readdir(self, path, fh):
        return ['.', '..'] + os.listdir(self.p(path))

    def readlink(self, path):
        return os.readlink(self.p(path))

    def release(self, path, fh):
        return self.from_slave(op=FuseChange.RELEASE, path=path,
                               fh_uuid=self.files[fh].uuid)

    def rename(self, old, new):
        # XXX: not idempotent! should be unlink/write[] ??
        raise FuseOSError(ENOTSUP)

    def rmdir(self, path):
        return self.from_slave(
            op=FuseChange.RMDIR,
            path=path,
        )

    def statfs(self, path):
        stv = os.statvfs(path)
        return dict((key, getattr(stv, key)) for key in (
            'f_bavail', 'f_bfree', 'f_blocks', 'f_bsize', 'f_favail',
            'f_ffree', 'f_files', 'f_flag', 'f_frsize', 'f_namemax'
        ))

    def symlink(self, path, src):
        return self.from_slave(op=FuseChange.SYMLINK, path=path, src=src)

    def truncate(self, path, length, fh=None):
        return self.from_slave(op=FuseChange.TRUNCATE, path=path, length=length)

    def unlink(self, path):
        return self.from_slave(op=FuseChange.UNLINK, path=path)

    def utimens(self, path, times):
        return self.from_slave(
            op=FuseChange.UTIME,
            path=path,
            atime=times[0],
            mtime=times[1],
        )

    def write(self, path, data, offset, fh):
        return self.from_slave(
            op=FuseChange.WRITE,
            path=path,
            data=data,
            offset=offset,
            fh_uuid=self.files[fh].uuid
        )
