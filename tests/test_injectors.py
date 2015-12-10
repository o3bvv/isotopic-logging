# -*- coding: utf-8 -*-

import unittest

from isotopic_logging.injectors import DirectPrefixInjector


class InjectorTestCaseBase(unittest.TestCase):
    strings = [
        "alpha",
        "bravo",
        "charlie",
    ]


class DirectPrefixInjectorTestCase(InjectorTestCaseBase):

    def test_direct_prefix_injector(self):
        injector = DirectPrefixInjector("foo > ")
        expected = [
            "foo > alpha",
            "foo > bravo",
            "foo > charlie",
        ]
        result = list(map(injector.mark, self.strings))
        self.assertEqual(result, expected)
