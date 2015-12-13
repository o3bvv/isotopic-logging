# -*- coding: utf-8 -*-

import threading
import unittest

from six import text_type, python_2_unicode_compatible
from six.moves import range

from isotopic_logging.concurrency import threadsafe_iter

from .utils import integers_generator


@python_2_unicode_compatible
class UnsafeIteratorError(Exception):

    def __init__(self, collisions_number):
        self.collisions_number = collisions_number
        super(UnsafeIteratorError, self).__init__()

    def __str__(self):
        return text_type("Iterator is not safe. Number of collisions: {0}."
                         .format(self.collisions_number))


class IteratorTester(object):

    def __init__(self, iterator):
        self.iterator = iterator
        self.threads = []
        self.errors = []

    def __call__(self, threads_count=100, calls_per_thread=500):
        for i in range(threads_count):
            t = threading.Thread(target=self._worker, args=(calls_per_thread,))
            self.threads.append(t)
            t.start()

        for t in self.threads:
            if t.is_alive():
                t.join()

        if self.errors:
            raise UnsafeIteratorError(len(self.errors))

    def _worker(self, calls_per_thread):
        for x in range(calls_per_thread):
            try:
                next(self.iterator)
            except ValueError as e:
                if text_type(e) != text_type("generator already executing"):
                    raise

                self.errors.append(e)


class ThreadsafeIterTestCase(unittest.TestCase):

    def test_threadsafe_iter(self):
        iterator = threadsafe_iter(integers_generator())
        tester = IteratorTester(iterator)

        try:
            tester()
        except UnsafeIteratorError as e:
            self.fail(text_type(e))
