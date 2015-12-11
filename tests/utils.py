# -*- coding: utf-8 -*-

import mock

from functools import wraps

from isotopic_logging.concurrency import threadsafe_iter


def patched_generate():
    i = 1
    while True:
        yield "gen-%d" % i
        i += 1


def patch_default_generator(call):

    @wraps(call)
    def decorator(*args, **kwargs):
        mock_generator = threadsafe_iter(patched_generate())

        def generate_oid(generator=None):
            return next(generator or mock_generator)

        # Patch object wich is already imported into `injectors` module
        patcher = mock.patch("isotopic_logging.injectors.generate_oid")
        mock_generate_prefix = patcher.start()
        mock_generate_prefix.side_effect = generate_oid

        try:
            call(*args, **kwargs)
        finally:
            patcher.stop()

    return decorator
