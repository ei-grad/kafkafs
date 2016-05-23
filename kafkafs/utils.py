from threading import Lock


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
