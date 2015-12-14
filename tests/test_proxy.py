# -*- coding: utf-8 -*-

import calendar
import logging
import time
import unittest

from freezegun import freeze_time
from mock import patch

from isotopic_logging.injectors import StaticPrefixInjector
from isotopic_logging.proxy import LoggerProxy


class LoggerProxyTestCase(unittest.TestCase):

    def setUp(self):
        patcher = patch('logging.Logger._log', return_value=None)
        self.patched_log = patcher.start()
        self.addCleanup(patcher.stop)

        self.original = logging.getLogger('logger_proxy_test')
        self.injector = StaticPrefixInjector("proxy test")
        self.testee = LoggerProxy(self.original, self.injector)

    @freeze_time("2015-01-01 01:23:45.670000")
    def test_proxy_elapsed_time(self):
        timetuple = time.strptime("2015-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        self.injector.enter_time = calendar.timegm(timetuple)

        actual = self.testee.elapsed_time
        expected = 1 * 60 * 60 + 23 * 60 + 45.67
        self.assertAlmostEqual(actual, expected, places=2)

    @freeze_time("2015-01-01 01:23:45.670000")
    def test_proxy_format_elapsed_time_default_format(self):
        timetuple = time.strptime("2015-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        self.injector.enter_time = calendar.timegm(timetuple)

        actual = self.testee.format_elapsed_time()
        self.assertEqual(actual, "01:23:45.670000")

    def test_proxy_plain_attribute(self):
        self.assertNotIn("log", self.testee.__dict__)
        self.testee.log(logging.DEBUG, "raw debug")
        self.patched_log.assert_called_with(
            logging.DEBUG, "raw debug", (),
        )
        self.assertNotIn("log", self.testee.__dict__)

    def test_proxy_default_logging_methods(self):
        method_names = [
            'debug', 'info', 'warn', 'warning', 'error', 'fatal', 'critical',
        ]

        for method_name in method_names:
            self.assertNotIn(method_name, self.testee.__dict__)
            getattr(self.testee, method_name)(method_name)

            level = getattr(logging, method_name.upper())
            message = "proxy test | {0}".format(method_name)

            self.patched_log.assert_called_with(level, message, (), )
            self.assertIn(method_name, self.testee.__dict__)

    def test_proxy_exception_helper(self):
        self.assertNotIn("exception", self.testee.__dict__)
        self.testee.exception("exception")
        self.patched_log.assert_called_with(
            logging.ERROR, "proxy test | exception", (), exc_info=1,
        )
        self.assertIn("exception", self.testee.__dict__)
