from threading import Lock
from functools import wraps
import os

from fuse import FuseOSError

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


def exc2fuse(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except OSError as e:
            raise FuseOSError(e.errno)
    return wrapper
