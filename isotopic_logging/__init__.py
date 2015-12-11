# -*- coding: utf-8 -*-

from .context import direct_injector, static_injector, auto_injector  # NOQA
from .context import hybrid_injector  # NOQA

# Import renamed factories for compatibility with previous versions
from .context import static_injector as prefix_injector  # NOQA
from .context import auto_injector as autoprefix_injector  # NOQA

from .generators import generate_oid, default_oid_generator  # NOQA
from .prefix import make_prefix, join_prefix  # NOQA
