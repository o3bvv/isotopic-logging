# -*- coding: utf-8 -*-


class PrefixInjector(object):

    __slots__ = ['prefix', ]

    def __init__(self, prefix):
        self.prefix = prefix

    def mark(self, message):
        return self.prefix + message
