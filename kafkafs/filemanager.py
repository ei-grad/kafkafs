from os.path import realpath
from threading import Lock
import os

from kafkafs.utils import flags_pbf2os


class FileManager():

    def __init__(self, root):
        self.lock = Lock()
        self.root = realpath(root)
        self._by_uuid = {}
        self._by_fh = {}

    def p(self, path):
        assert path[0] == '/'
        ret = os.path.join(self.root, path[1:])
        assert realpath(ret).startswith(self.root)
        return ret

    def add(self, handle):
        with self.lock:
            self._by_uuid[handle.uuid] = handle
            self._by_fh[handle.fh] = handle

    def open(self, uuid, path, flags, mode):
        if not isinstance(flags, int):
            flags = flags_pbf2os(flags)
        fh = os.open(self.p(path), flags, mode)
        self.add(FileHandle(
            path=path,
            uuid=uuid,
            flags=flags,
            fh=fh,
        ))
        return fh

    def __contains__(self, key):
        return key in self._by_uuid or key in self._by_fh

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._by_fh[key]
        else:
            return self._by_uuid[key]

    def __delitem__(self, key):
        with self.lock:
            if isinstance(key, int):
                fh = key
                uuid = self._by_fh[fh].uuid
            else:
                uuid = key
                fh = self._by_uuid[uuid].fh
            del self._by_fh[fh]
            del self._by_uuid[uuid]


class FileHandle():
    def __init__(self, path, uuid, flags, fh=None):
        self.path = path
        self.uuid = uuid
        self.flags = flags
        self.fh = fh

        self.lock = Lock()
