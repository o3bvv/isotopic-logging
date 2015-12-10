# -*- coding: utf-8 -*-

import mock
import unittest

from functools import wraps
from itertools import cycle

from isotopic_logging.injectors import (
    DirectPrefixInjector, SimplePrefixInjector, AutoprefixInjector,
)


def patch_default_generator(call):

    def generate():
        i = 1
        while True:
            yield "gen-%d" % i
            i += 1

    @wraps(call)
    def decorator(*args, **kwargs):

        mock_generator = generate()

        def generate_prefix(generator=None):
            return next(generator or mock_generator)

        patcher = mock.patch("isotopic_logging.injectors.generate_prefix")
        mock_generate_prefix = patcher.start()
        mock_generate_prefix.side_effect = generate_prefix

        try:
            call(*args, **kwargs)
        finally:
            patcher.stop()

    return decorator


class InjectorTestCaseBase(unittest.TestCase):
    strings = [
        "alpha",
        "bravo",
    ]

    def assert_injector(self, injector, expected_strings):
        result = list(map(injector.mark, self.strings))
        self.assertEqual(result, expected_strings)


class DirectPrefixInjectorTestCase(InjectorTestCaseBase):

    def test_injector(self):
        injector = DirectPrefixInjector("foo > ")
        expected = [
            "foo > alpha",
            "foo > bravo",
        ]
        self.assert_injector(injector, expected)


class SimplePrefixInjectorTestCase(InjectorTestCaseBase):

    def test_delimiter_is_default(self):
        injector = SimplePrefixInjector("foo")
        expected = [
            "foo | alpha",
            "foo | bravo",
        ]
        self.assert_injector(injector, expected)

    def test_delimiter_is_custom(self):
        injector = SimplePrefixInjector("foo", delimiter=":")
        expected = [
            "foo:alpha",
            "foo:bravo",
        ]
        self.assert_injector(injector, expected)


class AutoprefixInjectorTestCase(InjectorTestCaseBase):

    @patch_default_generator
    def test_all_parameters_are_default(self):
        injector = AutoprefixInjector()
        expected = [
            "gen-1 | alpha",
            "gen-1 | bravo",
        ]
        self.assert_injector(injector, expected)

        injector = AutoprefixInjector()
        expected = [
            "gen-2 | alpha",
            "gen-2 | bravo",
        ]
        self.assert_injector(injector, expected)

    def test_generator_is_custom(self):
        generator = cycle(["foo", "bar", ])

        injector = AutoprefixInjector(generator)
        expected = [
            "foo | alpha",
            "foo | bravo",
        ]
        self.assert_injector(injector, expected)

        injector = AutoprefixInjector(generator)
        expected = [
            "bar | alpha",
            "bar | bravo",
        ]
        self.assert_injector(injector, expected)

    @patch_default_generator
    def test_delimiter_is_custom(self):
        injector = AutoprefixInjector(delimiter=':')
        expected = [
            "gen-1:alpha",
            "gen-1:bravo",
        ]
        self.assert_injector(injector, expected)

    def test_all_parameters_are_custom(self):
        generator = cycle(["foo", "bar", ])

        injector = AutoprefixInjector(generator, delimiter=':')
        expected = [
            "foo:alpha",
            "foo:bravo",
        ]
        self.assert_injector(injector, expected)

        injector = AutoprefixInjector(generator, delimiter=':')
        expected = [
            "bar:alpha",
            "bar:bravo",
        ]
        self.assert_injector(injector, expected)
