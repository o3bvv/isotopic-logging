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
is populated from parrallel sources (threads or processes), and you need to
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


Important thing to note: each line of the example above may be logged in by
different functions running in different threads or processes. And they do not
need to remember and pass logging prefixes from one to another which keeps you
focused on development process and prevents you from distracting by log message
formatting.



Changelog
---------

* `2.0.0`_ (*pending*)

  * Feature: support nested prefixes (`issue #1`_).
  * Feature: simple and clean way to inject prefixes into calls to existing
    loggers (`issue #4`_).
  * Feature: ability to get context execution time (`issue #3`_).
  * Optimization: instances of injectors will be created only if new scope is
    defined (`issue #5`_).
  * Improvement: ensure prefix and target message are converted to strings
    during concatenation.
  * Renaming:

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

.. _OID_LENGTH: https://github.com/oblalex/isotopic-logging/blob/master/isotopic_logging/defaults.py#L3

.. _issue #1: https://github.com/oblalex/isotopic-logging/issues/1
.. _issue #2: https://github.com/oblalex/isotopic-logging/issues/2
.. _issue #3: https://github.com/oblalex/isotopic-logging/issues/3
.. _issue #4: https://github.com/oblalex/isotopic-logging/issues/4
.. _issue #5: https://github.com/oblalex/isotopic-logging/issues/5

.. _2.0.0: https://github.com/oblalex/isotopic-logging/compare/v1.0.1...v2.0.0
.. _1.0.1: https://github.com/oblalex/isotopic-logging/compare/v1.0.0...v1.0.1
.. _1.0.0: https://github.com/oblalex/isotopic-logging/releases/tag/v1.0.0
