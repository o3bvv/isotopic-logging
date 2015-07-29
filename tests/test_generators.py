# -*- coding: utf-8 -*-

import unittest
import traceback
import threading

from six.moves import range

from isotopic_logging.defaults import OID_LENGTH, OID_MAX_LENGTH
from isotopic_logging.generators import (
    generate_uuid_based_oid, default_oid_generator,
)


class UUIDBasedOIDGeneratorTestCase(unittest.TestCase):

    def test_default_length(self):
        g = generate_uuid_based_oid()
        oid = next(g)
        self.assertEqual(len(oid), OID_LENGTH)

    def test_min_length(self):
        g = generate_uuid_based_oid(length=None)
        oid = next(g)
        self.assertEqual(len(oid), OID_LENGTH)

        g = generate_uuid_based_oid(length=0)
        oid = next(g)
        self.assertEqual(len(oid), OID_LENGTH)

    def test_max_length(self):
        g = generate_uuid_based_oid(length=OID_MAX_LENGTH * 10)
        oid = next(g)
        self.assertEqual(len(oid), OID_MAX_LENGTH)


class DefaultOIDGeneratorTestCase(unittest.TestCase):

    def test_multitheading(self):

        def worker():
            for x in range(500):
                if stop_flag.isSet():
                    return

                try:
                    next(default_oid_generator)
                except Exception:
                    stop_flag.set()
                    errors.append(traceback.format_exc())
                    return

        threads, errors = [], []
        stop_flag = threading.Event()

        for i in range(100):
            t = threading.Thread(target=worker)
            threads.append(t)
            t.start()

        for t in threads:
            if t.is_alive():
                t.join()

        if errors:
            self.fail('\n'.join(errors))
