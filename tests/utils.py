# -*- coding: utf-8 -*-

import mock

from functools import wraps


def patch_default_generator(call):

    def generate():
        i = 1
        while True:
            yield "gen-%d" % i
            i += 1

    @wraps(call)
    def decorator(*args, **kwargs):

        mock_generator = generate()

        def generate_prefix(generator=None):
            return next(generator or mock_generator)

        # Patch object wich is already imported into `injectors` module
        patcher = mock.patch("isotopic_logging.injectors.generate_prefix")
        mock_generate_prefix = patcher.start()
        mock_generate_prefix.side_effect = generate_prefix

        try:
            call(*args, **kwargs)
        finally:
            patcher.stop()

    return decorator
