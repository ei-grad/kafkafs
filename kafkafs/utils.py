from threading import Lock
import os

from kafkafs.fuse_pb2 import FuseChange


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


class FileHandle():
    def __init__(self, path, uuid, flags, fh=None):
        self.path = path
        self.uuid = uuid
        self.flags = flags
        self.fh = fh
        self.lock = Lock()


def flags_pbf2os(flags):
    ret = 0
    for i in flags:
        ret |= getattr(os, FuseChange.Flag.Name(i))
    return ret


def flags_os2pbf(flags):
    ret = []
    for i in FuseChange.Flag.keys():
        if flags & getattr(os, i):
            ret.append(FuseChange.Flag.Value(i))
    return ret
