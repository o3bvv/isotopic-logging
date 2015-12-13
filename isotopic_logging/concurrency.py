# -*- coding: utf-8 -*-

import threading


class threadsafe_iter(object):
    """
    Takes an iterator/generator and makes it thread-safe by serializing call to
    the ``next`` method of given iterator/generator.
    """

    def __init__(self, original):
        self.original = original
        self.lock = threading.Lock()

    def __iter__(self):
        return self

    def __next__(self):
        with self.lock:
            return next(self.original)

    # Python 3 compatibility
    next = __next__
