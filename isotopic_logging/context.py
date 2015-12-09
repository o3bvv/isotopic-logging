# -*- coding: utf-8 -*-

from threading import local


_default_container = local()


class InjectionContext(object):

    def __init__(self, injector, container=None):
        self.container = container or _default_container
        self.is_top_level_call = not hasattr(self.container, '_injector')

        if self.is_top_level_call:
            self.container._injector = injector

    def __enter__(self):
        return self.container._injector

    def __exit__(self, type, value, traceback):
        if self.is_top_level_call:
            del self.container._injector
