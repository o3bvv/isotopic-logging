# -*- coding: utf-8 -*-

import unittest

from isotopic_logging.injectors import DirectPrefixInjector


class InjectorsTestCase(unittest.TestCase):

    def test_direct_prefix_injector(self):
        injector = DirectPrefixInjector("foo > ")

        strings = [
            "alpha",
            "bravo",
            "charlie",
        ]
        expected = [
            "foo > alpha",
            "foo > bravo",
            "foo > charlie",
        ]
        result = list(map(injector.mark, strings))
        self.assertEqual(result, expected)
