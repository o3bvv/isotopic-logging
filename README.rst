isotopic-logging
================

Mark and trace events in your log alike isotopic labeling.

|Build Status| |Coverage Status| |Quality| |PyPi package| |PyPi downloads|
|Python versions| |License|


**Table of contents**

.. contents::
    :local:
    :depth: 2
    :backlinks: none


Synopsis
--------

``isotopic-logging`` is a little Python library which may help you to cope with
everyday logging overhead.

Often you need to **track in time** some operation which consists of different
actions. Usually you enlog some information about those actions. And usually
those actions do not happen close to each other your code. Instead they happen
in different functions, modules or even packages. Considering this, you may
end up with logs where it's difficult to distinguish a separate operation.
And that's not good.

Usual solution is to put some message about operation into log entries, e.g. to
**add some prefix**. But here's a problem: even if your entire operation can be
placed into a single function, you still may need to stick a prefix into log
messages for multiple times. For example:

.. code-block:: python

    # Ugly logging example

    def some_operation(some_name):
        LOG.info("{0} | start".format(some_name))

        try:
            some_dangerous_action()
        except Exception as e:
            LOG.info("{0} | failure: {1}".format(some_name, e))
        else:
            LOG.info("{0} | success".format(some_name))
        finally:
            LOG.info("{0} | fullstop".format(some_name))

But, stop, hey, what's that smell? Yes, smells like copypasta spirit. And this
makes your eyes hurt.

Why this is ugly? Well, first of all, you need to follow same prefix pattern
all the time and everywhere in your project (and nobody cares how big it is).
It's a big responsibility and it's up to you. For example, it may happen you
put some extra space between prefix and message (or use another delimiter) and
you may miss something while using ``grep`` or so.

Secondly, you are doomed to drag that ``.format()`` with its arguments behind
each log message.

And yes, it will be a pain to change the way prefix is formatted and delimited
all over the project.

Moreover, if you decide to have same prefix to be used in **nested functions**,
then you will need to drag it through them. And this is a farewell to function
semantics and reusable code. You will not be able to cache or memoize functions
as well, because prefix may be constantly changing. In short, it's a recipe for
a disaster. So, for example:

.. code-block:: python

    # Passing auxiliary information through functions is quite ugly too

    def some_operation(arg1, arg2):
        prefix = "somehow calculed prefix"
        LOG.info("{0} | start".format(prefix))

        some_action1(arg1, arg2, prefix)
        some_action2(arg1, arg2, prefix)

        LOG.info("{0} | stop".format(prefix))

    def some_action1(arg1, arg2, _prefix):
        LOG.info("{0} | invoking some action".format(_prefix))

    def some_action2(arg1, arg2, _prefix):
        LOG.info("{0} | invoking some another action".format(_prefix))

As for me, such approach is **absolutely unacceptable**.

**As an administrator** I want to have log entries marked with same prefix
within single operation so that I can distinguish and track operations even if
log is written from multiple threads or sources.

**As a developer** I want to store prefix in some context so that I do not need
to format it per each call to logger and so that I can access it within nested
functions without passing prefix to a function directly and screwing up its
semantics.

So, how that can look like? Personally I propose the
**following alternatives**:

.. code-block:: python

    # Better and cleaner way to mark log entries

    def some_operation(some_name):
        with prefix_injector(some_name) as inj:
            LOG.info(inj.mark("start"))

            try:
                some_dangerous_action()
            except Exception as e:
                LOG.info(inj.mark(
                    "failure. Reason: {e}".format(e=e)))
            else:
                LOG.info(inj.mark("success"))
            finally:
                LOG.info(inj.mark("fullstop"))


Here we can see there is no more manual **prefix injection**. And it's easier
to read.

Second example and be rewritten as following:

.. code-block:: python

    # Contactless prefix transmission which does no harm to your functions

    def another_operation(arg1, arg2):
        with prefix_injector("somehow calculed prefix") as inj:
            LOG.info(inj.mark("start"))

            some_action1(arg1, arg2)
            some_action2(arg1, arg2)

            LOG.info(inj.mark("stop"))

    def some_action1(arg1, arg2):
        with autoprefix_injector() as inj:
            LOG.info(inj.mark("invoking some action"))

    def some_action2(arg1, arg2):
        with autoprefix_injector() as inj:
            LOG.info(inj.mark("invoking some another action"))


You can notice we do not pass **top-level prefix** into nested functions
directly. And this is good. Also, we specify default prefixes for them which is
good again. This allows us to reuse those functions. We can even memoize them
if we need.

So, with such approach we are able to write **less code** for log message
formatting, we can keep our **code modular and cleaner**, we can
**fallback to default prefixes** inside reusabe functions. All of this is
provided by usage of context managers which store prefixes in a special manner.

Having this, we are able to mark an operation by injection of a special
harmless prefix and then see in log how operation is executed through the
entire project's ecosystem. This is like `isotopic labeling`_. This is what I
call **isotopic logging**.

Welcome aboard!


Installation
------------

Simply get it at `Cheese Shop`_:

.. code-block:: bash

    pip install isotopic-logging


Usage
-----

    # TODO:


Customization
-------------

    # TODO:


Trivia
------

    # TODO:


Changelog
---------

* `1.0.0`_ (May 3, 2015)

  Initial version


.. |Build Status| image:: http://img.shields.io/travis/oblalex/isotopic-logging.svg?style=flat&branch=master
   :target: https://travis-ci.org/oblalex/isotopic-logging
.. |Coverage Status| image:: http://img.shields.io/coveralls/oblalex/isotopic-logging.svg?style=flat&branch=master
   :target: https://coveralls.io/r/oblalex/isotopic-logging?branch=master
.. |PyPi package| image:: http://img.shields.io/pypi/v/isotopic-logging.svg?style=flat
   :target: http://badge.fury.io/py/isotopic-logging/
.. |Quality| image:: https://scrutinizer-ci.com/g/oblalex/isotopic-logging/badges/quality-score.png?b=master&style=flat
   :target: https://scrutinizer-ci.com/g/oblalex/isotopic-logging/?branch=master
   :alt: Scrutinizer Code Quality
.. |PyPi downloads| image::  http://img.shields.io/pypi/dm/isotopic-logging.svg?style=flat
   :target: https://crate.io/packages/isotopic-logging/
.. |Python versions| image:: https://img.shields.io/badge/Python-2.6,2.7,3.3,3.4-brightgreen.svg?style=flat
   :alt: Supported versions of Python
.. |License| image:: https://img.shields.io/badge/license-LGPLv3-blue.svg?style=flat
   :target: https://github.com/oblalex/isotopic-logging/blob/master/LICENSE


.. _Cheese Shop: https://pypi.python.org/pypi/isotopic-logging
.. _Isotopic labeling: http://en.wikipedia.org/wiki/Isotopic_labeling

.. _1.0.0: https://github.com/oblalex/isotopic-logging/releases/tag/v1.0.0
