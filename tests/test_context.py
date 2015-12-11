# -*- coding: utf-8 -*-

import itertools
import unittest

from isotopic_logging.context import (
    InjectionContext, direct_injector, static_injector, auto_injector,
    hybrid_injector,
)
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
            "gen-1 | gen-2 | suboperation runs",
            "gen-1 | another nested call runs",
            "gen-1 | gen-3 | another suboperation starts",
            "gen-1 | gen-3 | gen-4 | another suboperation deeper runs",
            "gen-1 | gen-3 | another suboperation ends",
            "gen-1 | yet another nested call runs",
            "gen-1 | top operation ends",
        ]
        results = []

        def lazy_injector():
            return AutoprefixInjector()

        def top_operation():
            with InjectionContext(lazy_injector) as inj:
                results.append(inj.mark("top operation starts"))
                nested_call()
                suboperation()
                another_nested_call()
                another_suboperation()
                yet_another_nested_call()
                results.append(inj.mark("top operation ends"))

        def suboperation():
            with InjectionContext(lazy_injector, inherit=True) as inj:
                results.append(inj.mark("suboperation runs"))

        def nested_call():
            with InjectionContext(lazy_injector) as inj:
                results.append(inj.mark("nested call runs"))

        def another_nested_call():
            with InjectionContext(lazy_injector) as inj:
                results.append(inj.mark("another nested call runs"))

        def another_suboperation():
            with InjectionContext(lazy_injector, inherit=True) as inj:
                results.append(inj.mark("another suboperation starts"))
                another_suboperation_deeper()
                results.append(inj.mark("another suboperation ends"))

        def another_suboperation_deeper():
            with InjectionContext(lazy_injector, inherit=True) as inj:
                results.append(inj.mark("another suboperation deeper runs"))

        def yet_another_nested_call():
            with InjectionContext(lazy_injector) as inj:
                results.append(inj.mark("yet another nested call runs"))

        top_operation()
        self.assertEqual(results, expected)


class InjectionContextFactoriesTestCase(unittest.TestCase):

    def test_direct_injector(self):
        with direct_injector("foo") as inj:
            s = inj.mark("bar")
            self.assertEqual(s, "foobar")

    def test_prefix_injector(self):
        with static_injector("foo") as inj:
            s = inj.mark("bar")
            self.assertEqual(s, "foo | bar")

    @patch_default_generator
    def test_autoprefix_injector(self):
        with auto_injector() as inj:
            s = inj.mark("foo")
            self.assertEqual(s, "gen-1 | foo")

        with auto_injector() as inj:
            s = inj.mark("foo")
            self.assertEqual(s, "gen-2 | foo")

    @patch_default_generator
    def test_hybrid_injector(self):
        with hybrid_injector("something") as inj:
            s = inj.mark("foo")
            self.assertEqual(s, "gen-1 | something | foo")

        with hybrid_injector("something") as inj:
            s = inj.mark("foo")
            self.assertEqual(s, "gen-2 | something | foo")

    def test_nested_scopes_preserve_top_injector(self):
        args_map = {
            static_injector: ("foo", ),
            auto_injector: (),
            hybrid_injector: ("foo", ),
        }

        def new_injector(injector):
            return injector(*args_map[injector])

        def tester(args):
            injector1, injector2, injector3 = args

            with new_injector(injector1) as inj1:
                string1 = inj1.mark("bar")

                with new_injector(injector2) as inj2:
                    string2 = inj2.mark("bar")

                    with new_injector(injector3) as inj3:
                        string3 = inj3.mark("bar")

            self.assertEqual(string1, string2)
            self.assertEqual(string2, string3)

        map(tester, itertools.permutations(args_map.keys()))

    def test_prefix_transmission(self):

        def suboperation_in_another_thread_or_process(parent_prefix):
            with direct_injector(parent_prefix) as inj:
                return inj.mark("foo")

        with auto_injector() as inj:
            string1 = inj.mark("foo")
            prefix = inj.prefix

        string2 = suboperation_in_another_thread_or_process(prefix)

        self.assertEqual(string1, string2)

    @patch_default_generator
    def test_scope_inheritance(self):
        expected = [
            "gen-1 | Operation has started",
            "gen-1 | Nested call 1",
            "gen-1 | Phase 1 | Phase 1 runs",
            "gen-1 | Nested call 2",
            "gen-1 | Phase 2 | Phase 2 has started",
            "gen-1 | Phase 2 | Nested call 1 in phase 2",
            "gen-1 | Phase 2 | gen-2 | Parallel remote task 1",
            "gen-1 | Phase 2 | gen-3 | Parallel remote task 2",
            "gen-1 | Phase 2 | gen-4 | Parallel remote task 3",
            "gen-1 | Phase 2 | Nested call 2 in phase 2",
            "gen-1 | Phase 2 | Phase 2 has finished",
            "gen-1 | Nested call 3",
            "gen-1 | Operation has finished",
        ]
        results = []

        def operation():
            with auto_injector() as inj:
                results.append(inj.mark("Operation has started"))
                nested_call_1()
                phase_1()
                nested_call_2()
                phase_2()
                nested_call_3()
                results.append(inj.mark("Operation has finished"))

        def nested_call_1():
            with auto_injector() as inj:
                results.append(inj.mark("Nested call 1"))

        def phase_1():
            with static_injector("Phase 1", inherit=True) as inj:
                results.append(inj.mark("Phase 1 runs"))

        def nested_call_2():
            with auto_injector() as inj:
                results.append(inj.mark("Nested call 2"))

        def phase_2():
            with static_injector("Phase 2", inherit=True) as inj:
                results.append(inj.mark("Phase 2 has started"))
                phase_2_nested_call_1()

                for n in [1, 2, 3]:
                    phase_2_subphase(n)

                phase_2_nested_call_2()
                results.append(inj.mark("Phase 2 has finished"))

        def phase_2_nested_call_1():
            with auto_injector() as inj:
                results.append(inj.mark("Nested call 1 in phase 2"))

        def phase_2_subphase(n):
            with auto_injector(inherit=True) as inj:
                results.append(inj.mark(
                    "Parallel remote task {0}".format(n)))

        def phase_2_nested_call_2():
            with auto_injector() as inj:
                results.append(inj.mark("Nested call 2 in phase 2"))

        def nested_call_3():
            with auto_injector() as inj:
                results.append(inj.mark("Nested call 3"))

        operation()
        self.assertEqual(expected, results)
