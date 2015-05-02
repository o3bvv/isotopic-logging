# -*- coding: utf-8 -*-

import uuid

from .defaults import OID_LENGTH, OID_MAX_LENGTH


class UUIDBasedOIDGenerator(object):
    """
    OID generator which uses uuid.uuid4 (random UUIDs) to produce result.
    """

    def __init__(self, length=None):
        self.length = min(length or OID_LENGTH, OID_MAX_LENGTH)

    def __call__(self):
        return uuid.uuid4().hex.upper()[:self.length]


default_oid_generator_class = UUIDBasedOIDGenerator
default_oid_generator = default_oid_generator_class()
