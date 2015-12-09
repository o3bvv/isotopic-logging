# -*- coding: utf-8 -*-

import unittest

from isotopic_logging.injectors import DirectPrefixInjector


class InjectorsTestCase(unittest.TestCase):

    def test_direct_prefix_injector(self):
        injector = DirectPrefixInjector("foo > ")

        self.assertEqual(injector.mark("alpha"), "foo > alpha")
        self.assertEqual(injector.mark("bravo"), "foo > bravo")
        self.assertEqual(injector.mark("charlie"), "foo > charlie")
