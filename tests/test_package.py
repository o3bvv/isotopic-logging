# -*- coding: utf-8 -*-

import itertools
import unittest

from isotopic_logging import (
    direct_injector, prefix_injector, autoprefix_injector, hybrid_injector,
)

from .utils import patch_default_generator


class PackageTestCase(unittest.TestCase):

    def test_direct_injector(self):
        with direct_injector("foo") as inj:
            s = inj.mark("bar")
            self.assertEqual(s, "foobar")

    def test_prefix_injector(self):
        with prefix_injector("foo") as inj:
            s = inj.mark("bar")
            self.assertEqual(s, "foo | bar")

    @patch_default_generator
    def test_autoprefix_injector(self):
        with autoprefix_injector() as inj:
            s = inj.mark("foo")
            self.assertEqual(s, "gen-1 | foo")

        with autoprefix_injector() as inj:
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
            prefix_injector: ("foo", ),
            autoprefix_injector: (),
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

        with autoprefix_injector() as inj:
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
            with autoprefix_injector() as inj:
                results.append(inj.mark("Operation has started"))
                nested_call_1()
                phase_1()
                nested_call_2()
                phase_2()
                nested_call_3()
                results.append(inj.mark("Operation has finished"))

        def nested_call_1():
            with autoprefix_injector() as inj:
                results.append(inj.mark("Nested call 1"))

        def phase_1():
            with prefix_injector("Phase 1", inherit=True) as inj:
                results.append(inj.mark("Phase 1 runs"))

        def nested_call_2():
            with autoprefix_injector() as inj:
                results.append(inj.mark("Nested call 2"))

        def phase_2():
            with prefix_injector("Phase 2", inherit=True) as inj:
                results.append(inj.mark("Phase 2 has started"))
                phase_2_nested_call_1()

                for n in [1, 2, 3]:
                    phase_2_subphase(n)

                phase_2_nested_call_2()
                results.append(inj.mark("Phase 2 has finished"))

        def phase_2_nested_call_1():
            with autoprefix_injector() as inj:
                results.append(inj.mark("Nested call 1 in phase 2"))

        def phase_2_subphase(n):
            with autoprefix_injector(inherit=True) as inj:
                results.append(inj.mark(
                    "Parallel remote task {0}".format(n)))

        def phase_2_nested_call_2():
            with autoprefix_injector() as inj:
                results.append(inj.mark("Nested call 2 in phase 2"))

        def nested_call_3():
            with autoprefix_injector() as inj:
                results.append(inj.mark("Nested call 3"))

        operation()
        self.assertEqual(expected, results)
