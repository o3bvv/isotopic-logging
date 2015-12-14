# -*- coding: utf-8 -*-

import calendar
import time
import unittest

from itertools import cycle
from freezegun import freeze_time

from isotopic_logging.injectors import (
    DirectPrefixInjector, StaticPrefixInjector, AutoprefixInjector,
    HybridPrefixInjector, merge_injectors,
)

from .utils import patch_default_generator


class InjectorTestCaseBase(unittest.TestCase):
    strings = [
        "alpha",
        "bravo",
    ]

    def assert_mark(self, injector, expected_strings):
        result = list(map(injector.mark, self.strings))
        self.assertEqual(result, expected_strings)


class DirectPrefixInjectorTestCase(InjectorTestCaseBase):

    def test_mark(self):
        injector = DirectPrefixInjector("foo > ")
        expected = [
            "foo > alpha",
            "foo > bravo",
        ]
        self.assert_mark(injector, expected)

    def test_repr(self):
        injector = DirectPrefixInjector("the_prefix")

        actual = repr(injector)
        expected = """<isotopic_logging.injectors.DirectPrefixInjector("the_prefix")>"""
        self.assertEqual(actual, expected)

    def test_elapsed_time_out_context(self):
        injector = DirectPrefixInjector("prefix")
        self.assertRaises(ValueError, lambda: injector.elapsed_time)

    @freeze_time("2015-01-01 01:23:45.670000")
    def test_elapsed_time(self):
        injector = DirectPrefixInjector("prefix")

        timetuple = time.strptime("2015-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        injector.enter_time = calendar.timegm(timetuple)

        actual = injector.elapsed_time
        expected = 1 * 60 * 60 + 23 * 60 + 45.67
        self.assertAlmostEqual(actual, expected, places=2)

    @freeze_time("2015-01-01 01:23:45.670000")
    def test_format_elapsed_time_default_format(self):
        injector = DirectPrefixInjector("prefix")

        timetuple = time.strptime("2015-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        injector.enter_time = calendar.timegm(timetuple)

        actual = injector.format_elapsed_time()
        self.assertEqual(actual, "01:23:45.670000")

    @freeze_time("2015-01-01 01:23:45.670000")
    def test_format_elapsed_time_custom_format(self):
        injector = DirectPrefixInjector("prefix")

        timetuple = time.strptime("2015-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        injector.enter_time = calendar.timegm(timetuple)

        custom_format = "%H/%M/%S"
        actual = injector.format_elapsed_time(custom_format)
        self.assertEqual(actual, "01/23/45")


class StaticPrefixInjectorTestCase(InjectorTestCaseBase):

    def test_delimiter_is_default(self):
        injector = StaticPrefixInjector("foo")
        expected = [
            "foo | alpha",
            "foo | bravo",
        ]
        self.assert_mark(injector, expected)

    def test_delimiter_is_custom(self):
        injector = StaticPrefixInjector("foo", delimiter=":")
        expected = [
            "foo:alpha",
            "foo:bravo",
        ]
        self.assert_mark(injector, expected)


class AutoprefixInjectorTestCase(InjectorTestCaseBase):

    @patch_default_generator
    def test_all_parameters_are_default(self):
        injector = AutoprefixInjector()
        expected = [
            "gen-1 | alpha",
            "gen-1 | bravo",
        ]
        self.assert_mark(injector, expected)

        injector = AutoprefixInjector()
        expected = [
            "gen-2 | alpha",
            "gen-2 | bravo",
        ]
        self.assert_mark(injector, expected)

    def test_generator_is_custom(self):
        generator = cycle(["foo", "bar", ])

        injector = AutoprefixInjector(generator)
        expected = [
            "foo | alpha",
            "foo | bravo",
        ]
        self.assert_mark(injector, expected)

        injector = AutoprefixInjector(generator)
        expected = [
            "bar | alpha",
            "bar | bravo",
        ]
        self.assert_mark(injector, expected)

    @patch_default_generator
    def test_delimiter_is_custom(self):
        injector = AutoprefixInjector(delimiter=':')
        expected = [
            "gen-1:alpha",
            "gen-1:bravo",
        ]
        self.assert_mark(injector, expected)

    def test_all_parameters_are_custom(self):
        generator = cycle(["foo", "bar", ])

        injector = AutoprefixInjector(generator, delimiter=':')
        expected = [
            "foo:alpha",
            "foo:bravo",
        ]
        self.assert_mark(injector, expected)

        injector = AutoprefixInjector(generator, delimiter=':')
        expected = [
            "bar:alpha",
            "bar:bravo",
        ]
        self.assert_mark(injector, expected)


class HybridPrefixInjectorTestCase(InjectorTestCaseBase):

    @patch_default_generator
    def test_all_parameters_are_default(self):
        injector = HybridPrefixInjector("static")
        expected = [
            "gen-1 | static | alpha",
            "gen-1 | static | bravo",
        ]
        self.assert_mark(injector, expected)

        injector = HybridPrefixInjector("static")
        expected = [
            "gen-2 | static | alpha",
            "gen-2 | static | bravo",
        ]
        self.assert_mark(injector, expected)

    def test_generator_is_custom(self):
        generator = cycle(["foo", "bar", ])

        injector = HybridPrefixInjector("static", generator)
        expected = [
            "foo | static | alpha",
            "foo | static | bravo",
        ]
        self.assert_mark(injector, expected)

        injector = HybridPrefixInjector("static", generator)
        expected = [
            "bar | static | alpha",
            "bar | static | bravo",
        ]
        self.assert_mark(injector, expected)

    @patch_default_generator
    def test_delimiter_is_custom(self):
        injector = HybridPrefixInjector("static", delimiter=':')
        expected = [
            "gen-1:static:alpha",
            "gen-1:static:bravo",
        ]
        self.assert_mark(injector, expected)

    def test_all_parameters_are_custom(self):
        generator = cycle(["foo", "bar", ])

        injector = HybridPrefixInjector("static", generator, delimiter=':')
        expected = [
            "foo:static:alpha",
            "foo:static:bravo",
        ]
        self.assert_mark(injector, expected)

        injector = HybridPrefixInjector("static", generator, delimiter=':')
        expected = [
            "bar:static:alpha",
            "bar:static:bravo",
        ]
        self.assert_mark(injector, expected)


@patch_default_generator
def test_merge_injectors():
    i1 = AutoprefixInjector()
    i2 = StaticPrefixInjector("suboperation")
    i3 = AutoprefixInjector()
    merged = merge_injectors(i1, i2, i3)
    assert merged.prefix == "gen-1 | suboperation | gen-2 | "
