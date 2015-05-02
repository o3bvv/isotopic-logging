# -*- coding: utf-8 -*-

import unittest


from isotopic_logging.defaults import OID_LENGTH, OID_MAX_LENGTH
from isotopic_logging.generators import UUIDBasedOIDGenerator


class UUIDBasedOIDGeneratorTestCase(unittest.TestCase):

    def test_default_length(self):
        oid = UUIDBasedOIDGenerator()()
        self.assertEqual(len(oid), OID_LENGTH)

    def test_min_length(self):
        oid = UUIDBasedOIDGenerator(length=None)()
        self.assertEqual(len(oid), OID_LENGTH)

        oid = UUIDBasedOIDGenerator(length=0)()
        self.assertEqual(len(oid), OID_LENGTH)

    def test_max_length(self):
        oid = UUIDBasedOIDGenerator(length=OID_MAX_LENGTH * 10)()
        self.assertEqual(len(oid), OID_MAX_LENGTH)
