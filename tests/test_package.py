# -*- coding: utf-8 -*-

import itertools
import unittest

from isotopic_logging import (
    direct_injector, prefix_injector, autoprefix_injector, hybrid_injector,
)


class PackageTestCase(unittest.TestCase):

    def test_direct_injector(self):
        with direct_injector("foo") as inj:
            self.assertEqual(inj.mark("bar"), "foobar")

    def test_prefix_injector(self):
        with prefix_injector("foo") as inj:
            self.assertEqual(inj.mark("bar"), "foo | bar")

    def test_autoprefix_injector(self):
        with autoprefix_injector() as inj:
            string1 = inj.mark("foo")

        with autoprefix_injector() as inj:
            string2 = inj.mark("foo")

        self.assertNotEqual(string1, string2)

    def test_hybrid_injector(self):
        with hybrid_injector("something") as inj:
            string1 = inj.mark("foo")
            self.assertTrue(" | something | " in string1)

        with hybrid_injector("something") as inj:
            string2 = inj.mark("foo")
            self.assertTrue(" | something | " in string2)

        self.assertNotEqual(string1, string2)

    def test_nested_injectors(self):
        args_map = {
            prefix_injector: ("foo", ),
            autoprefix_injector: (),
            hybrid_injector: ("foo", ),
        }

        def new_injector(injector):
            return injector(*args_map[injector])

        def tester(arg):
            injector1, injector2, injector3 = arg

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

        def imaginary_function_in_another_thread_or_process(parent_prefix):
            with direct_injector(parent_prefix) as inj:
                return inj.mark("foo")

        with autoprefix_injector() as inj:
            string1 = inj.mark("foo")
            prefix = inj.prefix

        string2 = imaginary_function_in_another_thread_or_process(prefix)

        self.assertEqual(string1, string2)
