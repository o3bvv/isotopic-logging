# -*- coding: utf-8 -*-

from .context import InjectionContext
from .injectors import (
    DirectPrefixInjector, SimplePrefixInjector, AutoprefixInjector,
    HybrydPrefixInjector,
)


def direct_injector(prefix, nested=False):
    injector = DirectPrefixInjector(prefix)
    return InjectionContext(injector, nested)


def prefix_injector(prefix, delimiter=None, nested=False):
    injector = SimplePrefixInjector(prefix, delimiter)
    return InjectionContext(injector, nested)


def autoprefix_injector(oid_generator=None, delimiter=None, nested=False):
    injector = AutoprefixInjector(oid_generator, delimiter)
    return InjectionContext(injector, nested)


def hybrid_injector(prefix, oid_generator=None, delimiter=None, nested=False):
    injector = HybrydPrefixInjector(prefix, oid_generator, delimiter)
    return InjectionContext(injector, nested)
