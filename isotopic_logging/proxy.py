# -*- coding: utf-8 -*-

import logging

from functools import wraps

from ._compat import PY3, string_types


if PY3:
    _wrapped_method_names = {
        name.lower()
        for name in logging._nameToLevel.keys()
    }
else:
    _wrapped_method_names = {
        name.lower()
        for name in logging._levelNames.keys()
        if isinstance(name, string_types)
    }

_wrapped_method_names.update({
    'exception',
})


class LoggerProxy(object):
    """
    Proxy for `logging.Logger` and classes inherited from it.

    Automatically injects prefixes to messages which are send to log.
    This reduces overhead of

        >>> logger.log_level(injector.mark("mesage"))

    just to

        >>> logger.log_level("message")
    """

    def __init__(self, logger, injector):
        self._original = logger
        self.injector = injector

    @property
    def elapsed_time(self):
        return self.injector.elapsed_time

    def __getattr__(self, name):
        """
        Get attribute of original logger or wrapped version of methods used
        for logging.

        We do not wrap calls to `debug`, `info`, etc. directly. This is because
        those levels are default, but their list may be extended, for example,
        like in case of `python-verboselogs` library.
        """
        result = getattr(self._original, name)

        if name in _wrapped_method_names:

            @wraps(result)
            def wrapper(message, *args, **kwargs):
                return result(self.injector.mark(message), *args, **kwargs)

            # Cache wrapper, so it won't be constructed again for future calls.
            setattr(self, name, wrapper)
            return wrapper

        return result
