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

        def patched_log(level, msg, args, exc_info=None, extra=None):
            self.messages.append((level, msg, ))

        self.messages = []

        patcher = patch('logging.Logger._log', side_effect=patched_log)
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
    def test_format_elapsed_time_default_format(self):
        timetuple = time.strptime("2015-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
        self.injector.enter_time = calendar.timegm(timetuple)

        actual = self.testee.format_elapsed_time()
        self.assertEqual(actual, "01:23:45.670000")
