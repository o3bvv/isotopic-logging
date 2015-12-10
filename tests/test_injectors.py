# -*- coding: utf-8 -*-

import mock
import unittest

from functools import wraps
from itertools import cycle

from isotopic_logging.injectors import (
    DirectPrefixInjector, SimplePrefixInjector, AutoprefixInjector,
)


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
        injector = SimplePrefixInjector("foo", delimiter="-")
        expected = [
            "foo-alpha",
            "foo-bravo",
        ]
        self.assert_injector(injector, expected)


def patch_default_generator(call):

    @wraps(call)
    def decorator(*args, **kwargs):
        mock_generator = cycle(["foo", "bar", ])

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


class AutoprefixInjectorTestCase(InjectorTestCaseBase):

    @patch_default_generator
    def test_all_parameters_are_default(self):
        injector = AutoprefixInjector()
        expected = [
            "foo | alpha",
            "foo | bravo",
        ]
        self.assert_injector(injector, expected)

        injector = AutoprefixInjector()
        expected = [
            "bar | alpha",
            "bar | bravo",
        ]
        self.assert_injector(injector, expected)

    def test_generator_is_custom(self):
        generator = cycle(["buz", "qux", ])

        injector = AutoprefixInjector(generator)
        expected = [
            "buz | alpha",
            "buz | bravo",
        ]
        self.assert_injector(injector, expected)

        injector = AutoprefixInjector(generator)
        expected = [
            "qux | alpha",
            "qux | bravo",
        ]
        self.assert_injector(injector, expected)

    @patch_default_generator
    def test_delimiter_is_custom(self):
        injector = AutoprefixInjector(delimiter='-')
        expected = [
            "foo-alpha",
            "foo-bravo",
        ]
        self.assert_injector(injector, expected)

    def test_all_parameters_are_custom(self):
        generator = cycle(["buz", "qux", ])

        injector = AutoprefixInjector(generator, delimiter='-')
        expected = [
            "buz-alpha",
            "buz-bravo",
        ]
        self.assert_injector(injector, expected)

        injector = AutoprefixInjector(generator, delimiter='-')
        expected = [
            "qux-alpha",
            "qux-bravo",
        ]
        self.assert_injector(injector, expected)
