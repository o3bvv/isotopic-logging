# -*- coding: utf-8 -*-

from .generators import generate_prefix
from .prefix import make_prefix, join_prefix


class DirectPrefixInjector(object):

    __slots__ = ['prefix', ]

    def __init__(self, prefix):
        self.prefix = prefix

    def mark(self, message):
        return self.prefix + message


class SimplePrefixInjector(DirectPrefixInjector):

    def __init__(self, prefix, delimiter=None):
        prefix = make_prefix(prefix, delimiter)
        super(SimplePrefixInjector, self).__init__(prefix)


class AutoprefixInjector(SimplePrefixInjector):

    def __init__(self, oid_generator=None, delimiter=None):
        autopart = generate_prefix(oid_generator)
        super(AutoprefixInjector, self).__init__(autopart, delimiter)


class HybrydPrefixInjector(DirectPrefixInjector):

    def __init__(self, prefix, oid_generator=None, delimiter=None):
        autopart = generate_prefix(oid_generator)
        prefix = join_prefix([autopart, prefix, ], delimiter)
        super(HybrydPrefixInjector, self).__init__(prefix)


def merge_injectors(*args):
    prefix = ''.join([x.prefix for x in args])
    return DirectPrefixInjector(prefix)
