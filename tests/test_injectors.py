# -*- coding: utf-8 -*-

import unittest

from isotopic_logging.injectors import PrefixInjector


class InjectorsTestCase(unittest.TestCase):

    def test_prefix_injector(self):
        injector = PrefixInjector("foo > ")

        self.assertEqual(injector.mark("alpha"), "foo > alpha")
        self.assertEqual(injector.mark("bravo"), "foo > bravo")
        self.assertEqual(injector.mark("charlie"), "foo > charlie")
