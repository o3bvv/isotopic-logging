# -*- coding: utf-8 -*-

from .defaults import DELIMITER


def make_prefix(prefix, delimiter=None):
    return prefix + (delimiter or DELIMITER)


def join_prefix(chunks, delimiter=None):
    delimeter = delimiter or DELIMITER
    return make_prefix(delimeter.join(chunks), delimeter)
