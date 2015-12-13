# -*- coding: utf-8 -*-

import time
import threading

from collections import deque, namedtuple

from .injectors import (
    DirectPrefixInjector, StaticPrefixInjector, AutoprefixInjector,
    HybrydPrefixInjector,
)
from .injectors import merge_injectors


StackItem = namedtuple('StackItem', ('injector', 'parent', ))


class InjectionLocalStack(threading.local):

    def __init__(self):
        self._container = deque()
        super(InjectionLocalStack, self).__init__()

    def push(self, item):
        self._container.append(item)

    def pop(self):
        return self._container.pop()

    @property
    def top(self):
        try:
            return self._container[-1]
        except IndexError:
            return None

    @property
    def is_empty(self):
        return not self._container


_stack = InjectionLocalStack()


class InjectionContext(object):

    _old_enter_time = None

    def __init__(self, injector, inherit=False):
        if _stack.is_empty:
            if callable(injector):
                injector = injector()

            self._push(injector)
        elif inherit:
            if callable(injector):
                injector = injector()

            injector = merge_injectors(_stack.top.injector, injector)
            self._push(injector)

    def _push(self, injector):
        item = StackItem(injector, self)
        _stack.push(item)

    def __enter__(self):
        inj = _stack.top.injector
        self._old_enter_time, inj.enter_time = inj.enter_time, time.time()
        return inj

    def __exit__(self, exc_type, value, traceback):
        item = _stack.top

        inj = item.injector
        inj.enter_time, self._old_enter_time = self._old_enter_time, None

        if item.parent is self:
            _stack.pop()


def direct_injector(prefix, inherit=False):
    return InjectionContext(
        lambda: DirectPrefixInjector(prefix),
        inherit)


def static_injector(prefix, delimiter=None, inherit=False):
    return InjectionContext(
        lambda: StaticPrefixInjector(prefix, delimiter),
        inherit)


def auto_injector(oid_generator=None, delimiter=None, inherit=False):
    return InjectionContext(
        lambda: AutoprefixInjector(oid_generator, delimiter),
        inherit)


def hybrid_injector(prefix, oid_generator=None, delimiter=None, inherit=False):
    return InjectionContext(
        lambda: HybrydPrefixInjector(prefix, oid_generator, delimiter),
        inherit)
