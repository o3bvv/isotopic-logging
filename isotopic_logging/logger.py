# -*- coding: utf-8 -*-

from contextlib import contextmanager

from .context import (
    direct_injector, static_injector, auto_injector, hybrid_injector,
)
from .proxy import LoggerProxy


@contextmanager
def _get_proxy(logger, injector_context):
    with injector_context as injector:
        yield LoggerProxy(logger, injector)


class IsotopicLogger(object):

    __slots__ = ['_original', ]

    def __init__(self, logger):
        self._original = logger

    def __getattr__(self, name):
        return getattr(self._original, name)

    def direct(self, *args, **kwargs):
        return self._get_proxy(direct_injector, *args, **kwargs)

    def static(self, *args, **kwargs):
        return self._get_proxy(static_injector, *args, **kwargs)

    def auto(self, *args, **kwargs):
        return self._get_proxy(auto_injector, *args, **kwargs)

    def hybrid(self, *args, **kwargs):
        return self._get_proxy(hybrid_injector, *args, **kwargs)

    def _get_proxy(self, context_factory, *args, **kwargs):
        context = context_factory(*args, **kwargs)
        return _get_proxy(self._original, context)
