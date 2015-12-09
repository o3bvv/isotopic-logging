# -*- coding: utf-8 -*-

import mock
import unittest

from isotopic_logging.context import InjectionContext


class ContextTestCase(unittest.TestCase):

    def test_injection_context_parallel(self):
        injector1 = mock.Mock()
        injector2 = mock.Mock()

        with InjectionContext(injector1) as inj:
            self.assertEqual(inj, injector1)

        with InjectionContext(injector2) as inj:
            self.assertEqual(inj, injector2)

    def test_injection_context_nested(self):
        injector1 = mock.Mock()
        injector2 = mock.Mock()

        with InjectionContext(injector1) as top_inj:
            self.assertEqual(top_inj, injector1)

            with InjectionContext(injector2) as inj:
                self.assertEqual(inj, injector1)

    def test_injection_context_safe_exit(self):
        injector1 = mock.Mock()
        injector2 = mock.Mock()

        with InjectionContext(injector1) as top_inj:

            def nested_injection():
                """
                Wrap code with function to use assertRaises in a manner
                compatible with Python 2.6.
                """
                with InjectionContext(injector2) as inj:
                    self.assertEqual(inj, injector2)

            self.assertRaises(AssertionError, nested_injection)
            self.assertEqual(top_inj, injector1)
