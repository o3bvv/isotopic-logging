# -*- coding: utf-8 -*-

from .context import InjectionContext
from .injectors import (
    DirectPrefixInjector, SimplePrefixInjector, AutoprefixInjector,
    HybrydPrefixInjector,
)


def direct_injector(prefix):
    injector = DirectPrefixInjector(prefix)
    return InjectionContext(injector)


def prefix_injector(prefix, delimiter=None):
    injector = SimplePrefixInjector(prefix, delimiter)
    return InjectionContext(injector)


def autoprefix_injector(oid_generator=None, delimiter=None):
    injector = AutoprefixInjector(oid_generator, delimiter)
    return InjectionContext(injector)


def hybrid_injector(prefix, oid_generator=None, delimiter=None):
    injector = HybrydPrefixInjector(prefix, oid_generator, delimiter)
    return InjectionContext(injector)
