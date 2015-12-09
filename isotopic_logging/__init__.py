# -*- coding: utf-8 -*-

from .context import InjectionContext
from .generators import default_oid_generator
from .injectors import PrefixInjector
from .prefix import make_prefix, join_prefix


def direct_injector(prefix, container=None):
    injector = PrefixInjector(prefix)
    return InjectionContext(injector, container)


def prefix_injector(prefix, delimiter=None, container=None):
    prefix = make_prefix(prefix, delimiter)
    injector = PrefixInjector(prefix)
    return InjectionContext(injector, container)


def autoprefix_injector(oid_generator=None, delimiter=None, container=None):
    autopart = next(oid_generator or default_oid_generator)
    return prefix_injector(autopart, delimiter, container)


def hybrid_injector(prefix, oid_generator=None, delimiter=None,
                    container=None):
    autopart = next(oid_generator or default_oid_generator)
    prefix = join_prefix([autopart, prefix, ], delimiter)
    injector = PrefixInjector(prefix)
    return InjectionContext(injector, container)
