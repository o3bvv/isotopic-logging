# -*- coding: utf-8 -*-

import unittest

from isotopic_logging.prefix import make_prefix, join_prefix


class PrefixTestCase(unittest.TestCase):

    def test_make_prefix(self):
        self.assertEqual(make_prefix("testee"), "testee | ")

    def test_make_prefix_custom_delimiter(self):
        self.assertEqual(make_prefix("testee", ": "), "testee: ")

    def test_join_prefix(self):
        self.assertEqual(join_prefix(["foo", "bar"]), "foo | bar | ")

    def test_join_prefix_custom_prefix(self):
        self.assertEqual(join_prefix(["foo", "bar"], "-"), "foo-bar-")
