# -*- coding: utf-8 -*-

import time

from .generators import generate_oid
from .prefix import make_prefix, join_prefix


class DirectPrefixInjector(object):

    __slots__ = ['prefix', 'enter_time', ]

    def __init__(self, prefix):
        self.prefix = prefix

        # `enter_time` will be set by context manager
        self.enter_time = None

    def mark(self, message):
        # Use `format` as it will automatically convert parameters to strings
        return "{0}{1}".format(self.prefix, message)

    @property
    def elapsed_time(self):
        if self.enter_time:
            return time.time() - self.enter_time


class StaticPrefixInjector(DirectPrefixInjector):

    def __init__(self, prefix, delimiter=None):
        prefix = make_prefix(prefix, delimiter)
        super(StaticPrefixInjector, self).__init__(prefix)


class AutoprefixInjector(StaticPrefixInjector):

    def __init__(self, oid_generator=None, delimiter=None):
        autopart = generate_oid(oid_generator)
        super(AutoprefixInjector, self).__init__(autopart, delimiter)


class HybrydPrefixInjector(DirectPrefixInjector):

    def __init__(self, prefix, oid_generator=None, delimiter=None):
        autopart = generate_oid(oid_generator)
        prefix = join_prefix([autopart, prefix, ], delimiter)
        super(HybrydPrefixInjector, self).__init__(prefix)


def merge_injectors(*args):
    prefix = ''.join([x.prefix for x in args])
    return DirectPrefixInjector(prefix)
