# -*- coding: utf-8 -*-

import unittest

from isotopic_logging.injectors import (
    DirectPrefixInjector, SimplePrefixInjector,
)


class InjectorTestCaseBase(unittest.TestCase):
    strings = [
        "alpha",
        "bravo",
    ]


class DirectPrefixInjectorTestCase(InjectorTestCaseBase):

    def test_injector(self):
        injector = DirectPrefixInjector("foo > ")
        expected = [
            "foo > alpha",
            "foo > bravo",
        ]
        result = list(map(injector.mark, self.strings))
        self.assertEqual(result, expected)


class SimplePrefixInjectorTestCase(InjectorTestCaseBase):

    def test_default_delimiter(self):
        injector = SimplePrefixInjector("foo")
        expected = [
            "foo | alpha",
            "foo | bravo",
        ]
        result = list(map(injector.mark, self.strings))
        self.assertEqual(result, expected)

    def test_custom_delimiter(self):
        injector = SimplePrefixInjector("[foo]", delimiter=' ')
        expected = [
            "[foo] alpha",
            "[foo] bravo",
        ]
        result = list(map(injector.mark, self.strings))
        self.assertEqual(result, expected)
