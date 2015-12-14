# -*- coding: utf-8 -*-

import logging
import unittest

from mock import patch

from isotopic_logging.injectors import (
    DirectPrefixInjector, StaticPrefixInjector, AutoprefixInjector,
    HybridPrefixInjector,
)
from isotopic_logging.logger import IsotopicLogger
from isotopic_logging.proxy import LoggerProxy

from .utils import patch_default_generator


class IsotopicLoggerTestCase(unittest.TestCase):

    def setUp(self):
        patcher = patch('logging.Logger._log', return_value=None)
        self.patched_log = patcher.start()
        self.addCleanup(patcher.stop)

        self.original = logging.getLogger('logger_test')
        self.testee = IsotopicLogger(self.original)

    def test_proxy_plain_attribute(self):
        self.assertNotIn("log", self.testee.__dict__)
        self.testee.log(logging.DEBUG, "raw debug")
        self.patched_log.assert_called_with(
            logging.DEBUG, "raw debug", (),
        )
        self.assertNotIn("log", self.testee.__dict__)

    def test_direct_prefix_injector_proxy_logger_context(self):
        with self.testee.direct("direct | ") as log:
            self.assertIsInstance(log, LoggerProxy)
            self.assertIsInstance(log.injector, DirectPrefixInjector)

            log.debug("debug")
            self.patched_log.assert_called_with(
                logging.DEBUG, "direct | debug", (),
            )

    def test_static_prefix_injector_proxy_logger_context(self):
        with self.testee.static("static") as log:
            self.assertIsInstance(log, LoggerProxy)
            self.assertIsInstance(log.injector, StaticPrefixInjector)

            log.debug("debug")
            self.patched_log.assert_called_with(
                logging.DEBUG, "static | debug", (),
            )

    @patch_default_generator
    def test_autoprefix_injector_proxy_logger_context(self):
        with self.testee.auto() as log:
            self.assertIsInstance(log, LoggerProxy)
            self.assertIsInstance(log.injector, AutoprefixInjector)

            log.debug("debug")
            self.patched_log.assert_called_with(
                logging.DEBUG, "gen-1 | debug", (),
            )

    @patch_default_generator
    def test_hybrid_prefix_injector_proxy_logger_context(self):
        with self.testee.hybrid("hybrid") as log:
            self.assertIsInstance(log, LoggerProxy)
            self.assertIsInstance(log.injector, HybridPrefixInjector)

            log.debug("debug")
            self.patched_log.assert_called_with(
                logging.DEBUG, "gen-1 | hybrid | debug", (),
            )
