isotopic-logging
================

|pypi_package| |pypi_downloads| |python_versions| |license|

|unix_build| |windows_build| |coverage_status|

|code_issues| |codeclimate| |codacy| |quality| |health| |requirements|


**Table of contents**

.. contents::
    :local:
    :depth: 2
    :backlinks: none


Synopsis
--------

``isotopic-logging`` is a little Python library which is designed to help you
to track separate operations and their parts within whole execution flow. This
is done by injecting operation prefixes at the beginning of log messages.

This library was born in depths of real projects which have web applications
and background task queues, each of which can have multiple workers. There are
two key points this library resolves:

- As administrator I want to have log entries marked with same prefix
  within single operation so that I can distinguish and track operations even
  if log is written from multiple threads or sources.
- As developer I want to store prefix in some context so that I do not need
  to format it per each call to logger and so that I can access it within
  nested function calls without passing prefix to a function directly and
  screwing up its semantics.

``isotopic-logging`` comes very useful when you have a single log stream, which
is populated from parallel sources (threads or processes), and you need to
detect flow of a single operation in a mess of interweaving log messages and to
distinguish different instances of the same operation.

The library can be useful for single-process and single-thread applications as
well. You may still need to detect operations and track their execution time
and you can do it well.


Quick output example
--------------------

For example, log of a single complex operation may look like this:

.. code-block::

  INFO     [2015-12-15 21:45:04,339] D6EF95 | Heavy task has started.
  DEBUG    [2015-12-15 21:46:36,148] D6EF95 | Checking user permissions.
  INFO     [2015-12-15 21:46:36,654] D6EF95 | Analysis | Analysis phase has started.
  DEBUG    [2015-12-15 21:46:41,756] D6EF95 | Analysis | Analysing current state of devices.
  DEBUG    [2015-12-15 21:46:42,959] D6EF95 | Analysis | Analysing new state of devices.
  DEBUG    [2015-12-15 21:46:47,565] D6EF95 | Analysis | Analysing changes.
  INFO     [2015-12-15 21:46:51,871] D6EF95 | Analysis | Analysis phase has finished.
  INFO     [2015-12-15 21:46:54,073] D6EF95 | Pushing data to central storage.
  INFO     [2015-12-15 21:46:55,278] D6EF95 | Communication | Communication phase has started.
  DEBUG    [2015-12-15 21:46:58,884] D6EF95 | Communication | Spreading out parallel subtasks for every involved device.
  DEBUG    [2015-12-15 21:47:02,089] D6EF95 | Communication | 478272 | Connecting to device #3.
  DEBUG    [2015-12-15 21:47:03,493] D6EF95 | Communication | 28B208 | Connecting to device #1.
  INFO     [2015-12-15 21:47:04,798] D6EF95 | Communication | 28B208 | Running job at device #1.
  DEBUG    [2015-12-15 21:47:10,501] D6EF95 | Communication | AE2677 | Connecting to device #2.
  INFO     [2015-12-15 21:47:12,501] D6EF95 | Communication | AE2677 | Running job at device #2.
  INFO     [2015-12-15 21:47:17,707] D6EF95 | Communication | 478272 | Running job at device #3.
  INFO     [2015-12-15 21:47:21,709] D6EF95 | Communication | Communication phase has finished.
  DEBUG    [2015-12-15 21:47:24,412] D6EF95 | Commiting changes.
  INFO     [2015-12-15 21:47:27,013] D6EF95 | Heavy task has finished, elapsed time: 00:23:11.004120.


Important thing to note: each line of the example log from above may be
produced by different functions running in different threads or processes. And
they do not need to remember and pass logging prefixes from one to another
which keeps you focused on development process and prevents you from
distracting by log message formatting.


Installation
------------

To install the library simply get it at `Cheese Shop`_ (PyPI):

.. code-block:: bash

    pip install isotopic-logging


Key concepts
------------

Work of this library is based on several key concepts:

- Prefix injectors: they store or/and generate prefixes and inject them into
  strings.
- Injection contexts: they manage injectors (get or create them) and track
  scope execution time.
- Injection scopes: they drive creation of injectors and bound operation
  execution time.
- Logger wrapper: culmination of other concepts. Wraps loggers and provides
  methods for creation of injection contexts.

These concepts may be used separately or as a whole combination in form of
logger wrapper. Such approach is useful for flexible customization.


Prefix injectors
----------------

Prefix injectors are objects which store or/and generate prefixes accessed by
``prefix`` attribute and which are injected into target strings using
``mark()`` method.

Default injectors are defined in ``isotopic_logging.injectors`` module and they
are described below.


Direct prefix injector
~~~~~~~~~~~~~~~~~~~~~~

``DirectPrefixInjector`` will inject into strings exactly given prefix:

.. code-block:: python

  from isotopic_logging.injectors import DirectPrefixInjector

  inj = DirectPrefixInjector("foo > ")
  inj.mark("message")
  # "foo > message"

All other injectors are subclasses of ``DirectPrefixInjector`` and usually you
will not need to use it directly. Exception is only the case when you need to
transmit prefix between processes or threads.


Static prefix injector
~~~~~~~~~~~~~~~~~~~~~~

``StaticPrefixInjector`` automatically inserts delimiter between prefix and
target strings:

.. code-block:: python

  from isotopic_logging.injectors import StaticPrefixInjector

  inj = StaticPrefixInjector("foo")
  inj.mark("message")
  # "foo | message"

Default delimiter is defined as ``isotopic_logging.defaults.DELIMITER`` as its
value is ``" | "`` (space-pipe-space).

You can set custom delimiter:

.. code-block:: python

  inj = StaticPrefixInjector("foo", delimiter=":")
  inj.mark("message")
  # "foo:message"


Autoprefix injector
~~~~~~~~~~~~~~~~~~~

``AutoprefixInjector`` works like ``StaticPrefixInjector``, but it generates
prefixes by itself.

Generally it is used to distinguish different instances of same operations or
different calls to same methods and so on.

.. code-block:: python

  from isotopic_logging.injectors import AutoprefixInjector

  inj1 = AutoprefixInjector()
  inj1.mark("message")
  # "C220A0 | message"

  inj2 = AutoprefixInjector()
  inj2.mark("message")
  # "4118BB | message"

Here you can see that 2 different injectors have 2 different prefixes.

Default prefixes are generated by threadsafe generator
``isotopic_logging.generators.default_oid_generator`` which uses ``uuid.uuid4``
to produce results.

Given default prefix lenght of 6 symbols, default generator guarantees that 99%
of generated prefixes will be unique in case of 500 serial calls from 100
parallel threads. It is considered to be enough to distinguish operations which
are placed in time close to each other.

You can use custom generator:

.. code-block:: python

  from itertools import cycle
  from isotopic_logging.injectors import AutoprefixInjector

  generator = cycle(["foo", "bar", ])

  inj1 = AutoprefixInjector(generator)
  inj1.mark("message")
  # "foo | message"

  inj2 = AutoprefixInjector(generator)
  inj2.mark("message")
  # "bar | message"


If you are sure you need custom generator, you must ensure that it's threadsafe.
You can use ``isotopic_logging.concurrency.threadsafe_iter`` for this:

.. code-block:: python

  from isotopic_logging.concurrency import threadsafe_iter

  def generate():
      i = 1
      while True:
          yield "gen-%d" % i
          i += 1

  generator = threadsafe_iter(generate())

``threadsafe_iter`` is needed for generators which are implemented in pure
Python. For examle, in CPython ``itertools.cycle`` has native implementation
and it's threadsafe out of the box. Moreover, looks like Python 3 makes your
generators threadsafe as well, so it's quite possible that you will need
``threadsafe_iter`` only for Python 2.

``AutoprefixInjector`` also supports custom delimiters:

.. code-block:: python

  inj = AutoprefixInjector(delimiter=":")
  inj.mark("message")
  # "74D3B2:message"


Hybrid prefix injector
~~~~~~~~~~~~~~~~~~~~~~

``HybridPrefixInjector`` combines both features of ``AutoprefixInjector`` and
``StaticPrefixInjector``: it creates prefixes which consist of generated part
followed by static part which are separated by default or custom delimiter.

.. code-block:: python

  from isotopic_logging.injectors import HybridPrefixInjector

  inj1 = HybridPrefixInjector("static")
  inj1.mark("message")
  # "78E519 | static | message"

  inj2 = HybridPrefixInjector("static")
  inj2.mark("message")
  # "EF8A74 | static | message"

This prefix injector also supports custom delimiter and generator:

.. code-block:: python

  from itertools import cycle
  from isotopic_logging.injectors import HybridPrefixInjector

  generator = cycle(["foo", "bar", ])

  inj1 = HybridPrefixInjector("static", generator, delimiter=":")
  inj1.mark("message")
  # "foo:static:message"

  inj2 = HybridPrefixInjector("static", generator, delimiter=":")
  inj2.mark("message")
  # "bar:static:message"


Injection contexts
------------------

Injection contexts are used for scope management. Scopes are described in
the next section.

Contexts are responsible for providing you with proper injectors. Injectors are
created on demand. Generally, this can be described as:

- "Give me *current injector* or create new specific one if there is no *current injector*"
- or "Create new injector inherited from *current one* despite anything".

Contexts orginize injectors into stacks. Stacks are thread-local and do not
interfere with each other. There is no limit for stack size. This should not be
a problem, because injectors are created lazily. This happens only if stack is
empty or if you explicitly want to inherit current prefix (usually to
distinguish suboperation).

*Current injector* is the injector on top of the stack in current thread.

Injection context managers are defined in ``isotopic_logging.context`` module.
There is a proper context manager for each type of prefix injector. Context
managers accept accept same arguments as injectors which they are going to
produce.

Examples:

.. code-block:: python

  from isotopic_logging.context import direct_injector, static_injector
  from isotopic_logging.context import auto_injector, hybrid_injector

  with direct_injector("foo > ") as inj:
      inj.mark("message")
      # "foo > message"

  with static_injector("foo") as inj:
      inj.mark("message")
      # "foo | message"

  with auto_injector() as inj:
      inj.mark("message")
      # "25EBB8 | message"

  with hybrid_injector("static") as inj:
      inj.mark("message")
      # "0F9A8F | static | message"


Injection scopes
----------------

Scopes are created by contexts and they are used to drive creation of
injectors. There are two kinds of scopes: top-level and nested. Nested scopes
allow inheritance of prefixes.

Let's look at examples to grab the idea.


Nested scopes
~~~~~~~~~~~~~

.. code-block:: python

  from isotopic_logging.context import auto_injector, hybrid_injector

  def helper():
      with auto_injector() as inj:
          print(inj.mark("call from helper"))

  def operation():
      with hybrid_injector("operation") as inj:
          print(inj.mark("start"))
          helper()
          print(inj.mark("end"))

Here we separate ``helper`` and ``operation`` functions. Both of them define
own scopes via context managers.

If ``helper`` is called directly, it's scope will be *top-level* and new
injector will be created for each call:

.. code-block:: python

  helper()
  # ED5ED5 | call from helper
  helper()
  # 14F7CE | call from helper

If ``helper`` will be called from ``operation``, it's scope will become
*nested* and it will reuse injector created within top-level scope:

.. code-block:: python

  operation()
  # A15324 | operation | start
  # A15324 | operation | call from helper
  # A15324 | operation | end

In this case ``inj`` in ``operation`` and ``inj`` in ``helper`` will be exactly
the same object.


Inherited scopes
~~~~~~~~~~~~~~~~

Nested scopes are good if they are used within reusable helpers, utils, etc.,
especially if they are small. If nested calls present some complex operations,
you may want to separate them with own prefixes, but preserve parent prefix.

You can inherit current prefix to do so:

.. code-block:: python

  from isotopic_logging.context import (
      auto_injector, static_injector, hybrid_injector,
  )

  def helper():
      with auto_injector() as inj:
          print(inj.mark("call from helper"))

  def suboperation():
      with static_injector("suboperation", inherit=True) as inj:
          print(inj.mark("start"))
          helper()
          print(inj.mark("end"))

  def operation():
      with hybrid_injector("operation") as inj:
          print(inj.mark("start"))
          suboperation()
          print(inj.mark("end"))

  operation()
  # 9F3A34 | operation | start
  # 9F3A34 | operation | suboperation | start
  # 9F3A34 | operation | suboperation | call from helper
  # 9F3A34 | operation | suboperation | end
  # 9F3A34 | operation | end

Here, ``suboperation`` uses ``static_injector`` with flag ``inherit=True``.
This creates new injector, which is a combination of parent prefix and given
static prefix. ``suboperation`` also calls ``helper`` which creates nested
injection scope, as in the previous example.

So, as you can see, one of the main benefits of the library is prefix
transmission between separated functions. In couple with prefix management,
this keeps API of your functions and their bodies clean, saves your time and
mental focus.


Logger wrapper
--------------

``isotopic_logging`` allows you to wrap your loggers to prevent you from typing
``inj.mark()`` every time you put some message to log. This saves space for
code and makes it more readable.

Wrapping is done via ``isotopic_logging.IsotopicLogger`` logger wrapper. It
wraps loggers which are instances of ``logging.Logger`` and its subclasses.

Wrapper provides methods for creation of logger proxies with predefined prefix
injectors:

- ``direct()`` for ``DirectPrefixInjector``;
- ``static()`` for ``StaticPrefixInjector``;
- ``auto()`` for ``AutoprefixInjector``;
- ``hybrid()`` for ``HybridPrefixInjector``.

These methods accept same parameters as proper injection context managers. They
return contex managers for getting logger proxies. Proxies act as usual loggers
and they wrap logging calls with specific prefix.

Example:

.. code-block:: python

  import logging

  from isotopic_logging import IsotopicLogger

  LOG = IsotopicLogger(logging.getLogger(__name__))

  with LOG.auto() as log:
      log.debug("debug message")
      log.info("info message")
      log.warning("warning message")
      log.error("error message")
      log.critical("critical message")

  # DEBUG    [2015-12-31 13:38:55,554] 4B9FB5 | debug message
  # INFO     [2015-12-31 13:38:55,554] 4B9FB5 | info message
  # WARNING  [2015-12-31 13:38:55,554] 4B9FB5 | warning message
  # ERROR    [2015-12-31 13:38:55,554] 4B9FB5 | error message
  # CRITICAL [2015-12-31 13:38:55,554] 4B9FB5 | critical message

Here, ``LOG.auto()`` produces context which creates logger proxy with injected
autoprefix.


Time tracking
-------------

Prefix injectors allow you to track execution time within scopes. They provide:

- ``elapsed_time`` attribute, which counts elapsed_time in seconds;
- ``format_elapsed_time()`` method, which can accept custom format to output
  elapsed time as a string.

Examples:

.. code-block:: python

  import time
  from isotopic_logging import auto_injector

  with auto_injector() as inj:
      time.sleep(0.1)
      print(inj.elapsed_time)

  # 0.105129003525

Nested and inherited scopes have own internal time tracking:

.. code-block:: python

  with auto_injector() as inj1:
      time.sleep(0.1)

      with auto_injector() as inj2:
          time.sleep(0.1)
          print("inj2", inj2.elapsed_time)

      print("inj1", inj1.elapsed_time)

  # ('inj2', 0.10514497756958008)
  # ('inj1', 0.2101149559020996)

Default formatting outputs hours, minutes, seconds and microseconds:

.. code-block:: python

  with auto_injector() as inj:
      time.sleep(0.1)
      print(inj.format_elapsed_time())

  # 00:00:00.105154

You can use custom format compatible with format of
``datetime.datetime.strftime()``:

.. code-block:: python

  format = "%H/%M/%S"

  with auto_injector() as inj:
      time.sleep(5)
      print(inj.format_elapsed_time(format))

  # 00/00/05


Interthread prefix transmission
-------------------------------

Sometimes you may need to pass operation prefix between threads or processes.
For example, you start operation by handling HTTP request and continue it in
a background worker.

This can be easily made by using injector's ``prefix`` attribute and
``DirectPrefixInjector``:

.. code-block:: python

  def suboperation_in_another_thread_or_process(parent_prefix):
      with direct_injector(parent_prefix) as inj:
          print(inj.mark("foo"))

  def operation():
      with auto_injector() as inj:
          print(inj.mark("foo"))
          suboperation_in_another_thread_or_process(inj.prefix)

  operation()

  # 3539DB | foo
  # 3539DB | foo


Changelog
---------

* `2.0.0`_ (*pending*)

  * Feature: support inherited prefixes (`issue #1`_).
  * Feature: simple and clean way to inject prefixes into calls to existing
    loggers (`issue #4`_).
  * Feature: ability to get context execution time (`issue #3`_).
  * Optimization: instances of injectors will be created only if new scope is
    defined (`issue #5`_).
  * Improvement: ensure prefix and target message are converted to strings
    during concatenation.
  * Renamings:

    - ``prefix_injector`` to ``static_injector``;
    - ``autoprefix_injector`` to ``auto_injector``;

    *Old names are preserved and still can be used*.
  * Reduction: remove optional ``container`` parameter from everywhere.

* `1.0.1`_ (Jul 30, 2015)

  * Fix: threading support for ``default_oid_generator`` which is used by
    default by ``autoprefix_injector`` and ``hybrid_injector`` (`issue #2`_).

* `1.0.0`_ (May 3, 2015)

  Initial version


.. |pypi_package| image:: http://img.shields.io/pypi/v/isotopic-logging.svg?style=flat
   :target: http://badge.fury.io/py/isotopic-logging/
   :alt: Latest PyPI package

.. |pypi_downloads| image:: http://img.shields.io/pypi/dm/isotopic-logging.svg?style=flat
   :target: https://crate.io/packages/isotopic-logging/
   :alt: Downloands of latest PyPI package

.. |python_versions| image:: https://img.shields.io/badge/Python-2.7,3.4-brightgreen.svg?style=flat
   :alt: Supported versions of Python

.. |license| image:: https://img.shields.io/badge/license-LGPLv3-blue.svg?style=flat
   :target: https://github.com/oblalex/isotopic-logging/blob/master/LICENSE

.. |unix_build| image:: http://img.shields.io/travis/oblalex/isotopic-logging.svg?style=flat&branch=master
   :target: https://travis-ci.org/oblalex/isotopic-logging
   :alt: Build status of the master branch on Unix

.. |windows_build| image:: https://ci.appveyor.com/api/projects/status/hopk502wokd0qdyb/branch/master?svg=true
   :target: https://ci.appveyor.com/project/oblalex/isotopic-logging
   :alt: Build status of the master branch on Windows

.. |coverage_status| image:: http://codecov.io/github/oblalex/isotopic-logging/coverage.svg?branch=master
   :target: http://codecov.io/github/oblalex/isotopic-logging?branch=master
   :alt: Test coverage

.. |code_issues| image:: https://www.quantifiedcode.com/api/v1/project/c5eb11f66c184f679d30b3e1b883ae6c/badge.svg
   :target: https://www.quantifiedcode.com/app/project/c5eb11f66c184f679d30b3e1b883ae6c
   :alt: Code issues

.. |codeclimate| image:: https://codeclimate.com/github/oblalex/isotopic-logging/badges/gpa.svg
   :target: https://codeclimate.com/github/oblalex/isotopic-logging
   :alt: Code Climate

.. |codacy| image:: https://api.codacy.com/project/badge/grade/802f334a292f45b2898d8777ad46b611
   :target: https://www.codacy.com/app/oblalex/isotopic-logging
   :alt: Codacy Code Review

.. |quality| image:: https://scrutinizer-ci.com/g/oblalex/isotopic-logging/badges/quality-score.png?b=master&style=flat
   :target: https://scrutinizer-ci.com/g/oblalex/isotopic-logging/?branch=master
   :alt: Scrutinizer Code Quality

.. |health| image:: https://landscape.io/github/oblalex/isotopic-logging/master/landscape.svg?style=flat
   :target: https://landscape.io/github/oblalex/isotopic-logging/master
   :alt: Code Health

.. |requirements| image:: https://requires.io/github/oblalex/isotopic-logging/requirements.svg?branch=master
   :target: https://requires.io/github/oblalex/isotopic-logging/requirements/?branch=master
   :alt: Requirements Status


.. _Cheese Shop: https://pypi.python.org/pypi/isotopic-logging
.. _Isotopic labeling: http://en.wikipedia.org/wiki/Isotopic_labeling


.. _2.0.0: https://github.com/oblalex/isotopic-logging/compare/v1.0.1...v2.0.0
.. _1.0.1: https://github.com/oblalex/isotopic-logging/compare/v1.0.0...v1.0.1
.. _1.0.0: https://github.com/oblalex/isotopic-logging/releases/tag/v1.0.0


.. _issue #1: https://github.com/oblalex/isotopic-logging/issues/1
.. _issue #2: https://github.com/oblalex/isotopic-logging/issues/2
.. _issue #3: https://github.com/oblalex/isotopic-logging/issues/3
.. _issue #4: https://github.com/oblalex/isotopic-logging/issues/4
.. _issue #5: https://github.com/oblalex/isotopic-logging/issues/5

