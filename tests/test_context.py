# -*- coding: utf-8 -*-

import unittest

from isotopic_logging.context import InjectionContext
from isotopic_logging.injectors import AutoprefixInjector

from .utils import patch_default_generator


class InjectionContextTestCase(unittest.TestCase):

    def test_injection_context_parallel(self):
        injector1 = AutoprefixInjector()
        injector2 = AutoprefixInjector()

        with InjectionContext(injector1) as inj:
            self.assertEqual(inj, injector1)

        with InjectionContext(injector2) as inj:
            self.assertEqual(inj, injector2)

    def test_injection_context_nested(self):
        injector1 = AutoprefixInjector()
        injector2 = AutoprefixInjector()

        with InjectionContext(injector1) as top_inj:
            self.assertEqual(top_inj, injector1)

            with InjectionContext(injector2) as inj:
                self.assertEqual(inj, injector1)

    def test_injection_context_safe_exit(self):
        injector1 = AutoprefixInjector()
        injector2 = AutoprefixInjector()

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

    @patch_default_generator
    def test_inheritance(self):
        expected = [
            "gen-1 | top operation starts",
            "gen-1 | nested call runs",
            "gen-1 | gen-3 | suboperation runs",
            "gen-1 | another nested call runs",
            "gen-1 | gen-5 | another suboperation starts",
            "gen-1 | gen-5 | gen-6 | another suboperation deeper runs",
            "gen-1 | gen-5 | another suboperation ends",
            "gen-1 | yet another nested call runs",
            "gen-1 | top operation ends",
        ]
        results = []

        def _top_operation():
            with InjectionContext(AutoprefixInjector()) as inj:
                results.append(inj.mark("top operation starts"))
                _nested_call()
                _suboperation()
                _another_nested_call()
                _another_suboperation()
                _yet_another_nested_call()
                results.append(inj.mark("top operation ends"))

        def _suboperation():
            with InjectionContext(AutoprefixInjector(), inherit=True) as inj:
                results.append(inj.mark("suboperation runs"))

        def _nested_call():
            with InjectionContext(AutoprefixInjector()) as inj:
                results.append(inj.mark("nested call runs"))

        def _another_nested_call():
            with InjectionContext(AutoprefixInjector()) as inj:
                results.append(inj.mark("another nested call runs"))

        def _another_suboperation():
            with InjectionContext(AutoprefixInjector(), inherit=True) as inj:
                results.append(inj.mark("another suboperation starts"))
                _another_suboperation_deeper()
                results.append(inj.mark("another suboperation ends"))

        def _another_suboperation_deeper():
            with InjectionContext(AutoprefixInjector(), inherit=True) as inj:
                results.append(inj.mark("another suboperation deeper runs"))

        def _yet_another_nested_call():
            with InjectionContext(AutoprefixInjector()) as inj:
                results.append(inj.mark("yet another nested call runs"))

        _top_operation()
        self.assertEqual(results, expected)
