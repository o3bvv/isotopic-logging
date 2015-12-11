# -*- coding: utf-8 -*-

import uuid

from .defaults import OID_LENGTH, OID_MAX_LENGTH
from .concurrency import threadsafe_iter


def generate_uuid_based_oid(length=None):
    """
    OID generator which uses uuid.uuid4 (random UUIDs) to produce result.
    """
    length = min(length or OID_LENGTH, OID_MAX_LENGTH)

    while True:
        yield uuid.uuid4().hex.upper()[:length]


generate_default_oid = generate_uuid_based_oid
default_oid_generator = threadsafe_iter(generate_default_oid())


def generate_oid(generator=None):
    return next(generator or default_oid_generator)
