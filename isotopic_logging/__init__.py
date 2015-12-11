# -*- coding: utf-8 -*-

from contextlib import contextmanager

from .context import InjectionContext
from .generators import generate_oid, default_oid_generator # NOQA
from .injectors import (
    DirectPrefixInjector, SimplePrefixInjector, AutoprefixInjector,
    HybrydPrefixInjector,
)
from .prefix import make_prefix, join_prefix # NOQA
from .proxy import InjectingLogger


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


@contextmanager
def wrap_logger(logger, injection_context):
    with injection_context as inj:
        yield InjectingLogger(logger, inj)
