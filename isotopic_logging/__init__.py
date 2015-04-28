# -*- coding: utf-8 -*-

from contextlib import contextmanager


class PrefixInjector(object):

    def __init__(self, details):
        self._prefix = self._get_prefix(details)

    @staticmethod
    def _get_prefix(details):
        prefix = ["smth", ]

        if details:
            prefix.append(details)

        prefix.append("")

        return " | ".join(prefix)

    def mark(self, message):
        return self._prefix + message


@contextmanager
def prefix_injector(details=None):
    yield PrefixInjector(details)
