# -*- coding: utf-8 -*-

from collections import deque, namedtuple
from threading import local

from .injectors import merge_injectors


StackItem = namedtuple('StackItem', ['injector', 'parent', ])


class InjectionStack(object):

    def __init__(self, local):
        local.stack = deque()
        self._local = local

    def push(self, item):
        self._local.stack.append(item)

    def pop(self):
        return self._local.stack.pop()

    @property
    def top(self):
        try:
            return self._local.stack[-1]
        except IndexError:
            return None

    @property
    def is_empty(self):
        return not self._local.stack


_local = local()
_stack = InjectionStack(_local)


class InjectionContext(object):

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
        return _stack.top.injector

    def __exit__(self, type, value, traceback):
        if _stack.top.parent is self:
            _stack.pop()
