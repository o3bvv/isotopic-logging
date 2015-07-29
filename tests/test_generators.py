# -*- coding: utf-8 -*-

import unittest

from isotopic_logging.defaults import OID_LENGTH, OID_MAX_LENGTH
from isotopic_logging.generators import generate_uuid_based_oid


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
