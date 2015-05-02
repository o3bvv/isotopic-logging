# -*- coding: utf-8 -*-

from contextlib import contextmanager
from threading import local


_default_container = local()


@contextmanager
def injection_context(injector, container=None):
    container = container or _default_container
    is_top_level_call = not hasattr(container, '_injector')

    if is_top_level_call:
        container._injector = injector

    try:
        yield container._injector
    except Exception as e:
        raise e
    finally:
        if is_top_level_call:
            del container._injector
