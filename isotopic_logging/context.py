# -*- coding: utf-8 -*-

from collections import deque, namedtuple
from threading import local


_stack_holder = local()

ScopeItem = namedtuple('ScopeItem', ['injector', 'parent'])


class InjectionContext(object):

    def __init__(self, injector, nested=False):
        if not hasattr(_stack_holder, '_stack'):
            _stack_holder._stack = deque()
            self._create_new_scope(injector)
        elif nested:
            self._create_new_scope(injector)

    def _create_new_scope(self, injector):
        item = ScopeItem(injector, self)
        _stack_holder._stack.append(item)

    def __enter__(self):
        return _stack_holder._stack[-1].injector

    def __exit__(self, type, value, traceback):
        if _stack_holder._stack[-1].parent is self:
            _stack_holder._stack.pop()

        if not _stack_holder._stack:
            del _stack_holder._stack
