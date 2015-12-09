# -*- coding: utf-8 -*-

from .context import InjectionContext
from .injectors import (
    DirectPrefixInjector, SimplePrefixInjector, AutoprefixInjector,
    HybrydPrefixInjector,
)


def direct_injector(prefix, container=None):
    injector = DirectPrefixInjector(prefix)
    return InjectionContext(injector, container)


def prefix_injector(prefix, delimiter=None, container=None):
    injector = SimplePrefixInjector(prefix, delimiter)
    return InjectionContext(injector, container)


def autoprefix_injector(oid_generator=None, delimiter=None, container=None):
    injector = AutoprefixInjector(oid_generator, delimiter)
    return InjectionContext(injector, container)


def hybrid_injector(prefix, oid_generator=None, delimiter=None,
                    container=None):
    injector = HybrydPrefixInjector(prefix, oid_generator, delimiter)
    return InjectionContext(injector, container)
