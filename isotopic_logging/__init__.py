# -*- coding: utf-8 -*-

from .context import InjectionContext
from .injectors import (
    DirectPrefixInjector, SimplePrefixInjector, AutoprefixInjector,
    HybrydPrefixInjector,
)


def direct_injector(prefix, inherit=False):
    injector = DirectPrefixInjector(prefix)
    return InjectionContext(injector, inherit)


def prefix_injector(prefix, delimiter=None, inherit=False):
    injector = SimplePrefixInjector(prefix, delimiter)
    return InjectionContext(injector, inherit)


def autoprefix_injector(oid_generator=None, delimiter=None, inherit=False):
    injector = AutoprefixInjector(oid_generator, delimiter)
    return InjectionContext(injector, inherit)


def hybrid_injector(prefix, oid_generator=None, delimiter=None, inherit=False):
    injector = HybrydPrefixInjector(prefix, oid_generator, delimiter)
    return InjectionContext(injector, inherit)
