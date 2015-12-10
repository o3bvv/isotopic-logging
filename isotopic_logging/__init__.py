# -*- coding: utf-8 -*-

from .context import InjectionContext
from .injectors import (
    DirectPrefixInjector, SimplePrefixInjector, AutoprefixInjector,
    HybrydPrefixInjector,
)


def direct_injector(prefix, inherit=False):
    return InjectionContext(
        lambda: DirectPrefixInjector(prefix),
        inherit)


def prefix_injector(prefix, delimiter=None, inherit=False):
    return InjectionContext(
        lambda: SimplePrefixInjector(prefix, delimiter),
        inherit)


def autoprefix_injector(oid_generator=None, delimiter=None, inherit=False):
    return InjectionContext(
        lambda: AutoprefixInjector(oid_generator, delimiter),
        inherit)


def hybrid_injector(prefix, oid_generator=None, delimiter=None, inherit=False):
    return InjectionContext(
        lambda: HybrydPrefixInjector(prefix, oid_generator, delimiter),
        inherit)
