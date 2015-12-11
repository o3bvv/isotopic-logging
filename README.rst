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

``isotopic-logging`` is a little Python library which may help you to cope with
everyday logging overhead.

Often you need to **track in time** some operation which consists of different
actions. Usually you enlog some information about those actions. And usually
those actions do not happen close to each other in your code. Instead, they may
happen in different functions, modules or even packages. Considering this, you
may end up with logs where it's difficult to distinguish a separate operation.
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

Stop, hey, what's that smell? Yes, smells like copypasta spirit. And this
makes your eyes hurt.

Why this is ugly? Well, first of all, you need to follow same prefix pattern
all the time and everywhere in your project (and nobody cares how big is it).
It's a big responsibility and it's up to you. For example, it may happen you
put some extra space between prefix and message (or use another delimiter) and
you may miss something while using ``grep`` or so.

Secondly, you are doomed to drag that ``.format()`` with its arguments behind
each log message.

And yes, it will be a pain to change the way prefix is formatted and delimited
all over the project.

Moreover, if you decide to have same prefix to be used in
**nested function calls**, then you will need to drag it through them. And this
is a farewell to function semantics and reusable code. You will not be able to
cache or memoize functions as well, because prefix may be constantly changing.
In short, it's a recipe for a disaster. So, for example:

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
function calls without passing prefix to a function directly and screwing up
its semantics.

So, how that can look like? Personally I propose the
**following alternatives**:

.. code-block:: python

    # Better and cleaner way to mark log entries

    def some_operation(some_name):
        with static_injector(some_name) as inj:
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
        with static_injector("somehow calculed prefix") as inj:
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


You can notice we do not pass **top-level prefix** into function calls
directly. And this is good. Also, we specify default prefixes for them which is
good again. This allows us to reuse those functions. We can even memoize them
if we need.

So, with such approach we are able to write **less code** for log message
formatting, we can keep our **code modular and cleaner**, we can
**fallback to default prefixes** inside reusabe functions. All of this is
provided by usage of context managers which store prefixes in a special manner.

Having this, we are able to mark an operation by injection of a special
harmless prefix into it and then see in log how operation is executed through
the entire project's ecosystem. This is like `isotopic labeling`_. This is what
I call **isotopic logging**.

Welcome aboard!


Installation
------------

Simply get it at `Cheese Shop`_:

.. code-block:: bash

    pip install isotopic-logging


Usage
-----

The main concept of this library is to define a **prefix injector** once and
then to ask it to **mark strings** in a same manner.

The library provides several default prefix injectors which are described
below.


Direct injector
~~~~~~~~~~~~~~~

``direct_injector`` adds exactly that prefix to strings which you tell it:

.. code-block:: python

    from isotopic_logging import direct_injector

    with direct_injector("foo") as inj:
        print(inj.mark("bar"))
        print(inj.mark("buz"))

    # Output:
    # "foobar"
    # "foobuz"


Prefix injector
~~~~~~~~~~~~~~~

``static_injector`` acts same way as ``direct_injector``, but in addition
it puts a delimiter between prefix and target message:

.. code-block:: python

    from isotopic_logging import static_injector

    with static_injector("foo") as inj:
        print(inj.mark("bar"))
        print(inj.mark("buz"))

    # Output:
    # "foo | bar"
    # "foo | buz"

As you see, default delimiter is ``" | "`` (space-pipe-space). You can change
it to something own:

.. code-block:: python

    with static_injector("foo", delimiter="::") as inj:
        print(inj.mark("bar"))
        print(inj.mark("buz"))

    # Output:
    # "foo::bar"
    # "foo::buz"


Autoprefix injector
~~~~~~~~~~~~~~~~~~~

If you just want to mark your message somehow and you do not care about how it
will be marked, then ``autoprefix_injector`` is at your service:

.. code-block:: python

    from isotopic_logging import autoprefix_injector

    with autoprefix_injector() as inj:
        print(inj.mark("foo"))
        print(inj.mark("bar"))

    with autoprefix_injector() as inj:
        print(inj.mark("buz"))

    # Output:
    # "E340F3 | foo:
    # "E340F3 | bar:
    # "172077 | buz:

Here we see that ``autoprefix_injector`` acts like ``static_injector``, but
instead of predefined prefix it uses something else. This something else is
called **operation ID** or ``OID``.

You can use your own ``OID`` generator by passing it via ``oid_generator``
argument (see section ``Customization`` -> ``Custom OID generators``).

And, of course, you can set your own ``delimiter`` also.


Hybrid injector
~~~~~~~~~~~~~~~

If you need to have some static prefix, but you want to make it a bit different
per each operation, then you may use ``hybrid_injector``. It acts like
``autoprefix_injector`` but allows you to have some static part as in case of
simple ``static_injector``:

.. code-block:: python

    from isotopic_logging import hybrid_injector

    with hybrid_injector("foo") as inj:
        print(inj.mark("bar"))
        print(inj.mark("buz"))

    with hybrid_injector("foo") as inj:
        print(inj.mark("qux"))

    # Output:
    # "EC9C6B | foo | bar"
    # "EC9C6B | foo | buz"
    # "59A8D6 | foo | qux"


``hybrid_injector`` can have custom ``oid_generator`` and custom ``delimiter``
as for previous injectors.


Nested function calls
~~~~~~~~~~~~~~~~~~~~~

This is the sugar part of the library. Imagine, you need to execute a single
operation passing through loosely-coupled or quite different pieces of code
(functions, objects, modules, etc). Well, this can be easy enough.

Say, you have some independent functions which log what they do:

.. code-block:: python

    def add(a, b):
        with autoprefix_injector() as inj:
            print(inj.mark(
                "adding {a} to {b}"
                .format(a=a, b=b)))

            result = a + b

            print(inj.mark(
                "resulting into {0}".format(result)))

            return result

    def multiply(a, b):
        with autoprefix_injector() as inj:
            print(inj.mark(
                "making production of {a} and {b}"
                .format(a=a, b=b)))

            result = a * b

            print(inj.mark(
                "resulting into {0}".format(result)))

            return result

You will get different prefixes if you run them separately:

.. code-block:: python

    add(1, 2)
    # Output:
    # "2C091F | adding 1 to 2"
    # "2C091F | resulting into 3"
    # 3

    multiply(1, 2)
    # Output:
    # "A15D88 | making production of 1 and 2"
    # "A15D88 | resulting into 2"
    # 2

And now let's define some funtion which aggregates both of that operations:

.. code-block:: python

    def add_and_multiply(a, b):
        with autoprefix_injector() as inj:
            print(inj.mark(
                "adding and multiplying {a} with {b}..."
                .format(a=a, b=b)))

            result = (add(a, b), multiply(a, b))

            print(inj.mark(
                "end result is {0}".format(result)))

            return result

If we call it, we'll see that all prefixes are inherited from top-level
function call:

.. code-block:: python

    add_and_multiply(1, 2)

    # Output:
    # "1543A0 | adding and multiplying 1 with 2..."
    # "1543A0 | adding 1 to 2"
    # "1543A0 | resulting into 3"
    # "1543A0 | making production of 1 and 2"
    # "1543A0 | resulting into 2"
    # "1543A0 | end result is (3, 2)"
    # (3, 2)

Yay! There's no mess with passing prefixes inside other functions!

This works not only with ``autoprefix_injector``: any type of prefix injectors
will work pretty fine.


Prefix transmission
~~~~~~~~~~~~~~~~~~~

Sometimes you may need to track some operation executed inside different
processes. For examaple, you handle some HTTP request and then start some
background job (say, via ``Celery``). In this case, you will need to pass
your prefix to another process.

Every injector has a ``prefix`` attribute, e.g.:

.. code-block:: python

    with autoprefix_injector() as inj:
        print(inj.prefix)

    # Output:
    # "08C22E | "

So, you are able to throw the prefix to a right place. How can you pick it up?
Well, this is the main purpose that ``direct_injector`` was created for. Let's
imitate prefix transmission:

.. code-block:: python

    from celery import shared_task
    from mock import Mock


    def add_view(request):
        with autoprefix_injector() as inj:
            username = request.user.username
            x, y = request.data['x'], request.data['y']

            LOG.info(inj.mark(
                "user '{username}' visits add_view() with x={x} and y={y} as "
                "arguments"
                .format(username=username, x=x, y=y)))

            add.async_apply((x, y, inj.prefix))


    @shared_task
    def add(x, y, _operation_prefix):
        with direct_injector(_operation_prefix) as inj:
            result =  x + y
            LOG.info(inj.mark(
                "{x} + {y} = {result}"
                .format(x=x, y=y, result=result)))
            return result


    request = Mock(
        user=Mock(username="abuser"),
        data=dict(x=1, y=2),
    )
    add_view(request)

    # Log output:
    # "C71F3F | user 'abuser' visits add_view() with x=1 and y=2 as arguments"
    # "C71F3F | 1 + 2 = 3"


Customization
-------------

Custom OID generators
~~~~~~~~~~~~~~~~~~~~~

By default ``OID`` is created by ``default_oid_generator``:

.. code-block:: python

    from isotopic_logging.generators import default_oid_generator

    for x in range(5):
        print(next(default_oid_generator))

    # Output:
    # "9592BC"
    # "58B974"
    # "9E403B"
    # "C180B2"
    # "C9FE44"

Default generator is an instance of ``isotopic_logging.generators.generate_uuid_based_oid``
with default `OID_LENGTH`_.

So, you can change the length of autogenerated prefix:

.. code-block:: python

    from isotopic_logging import autoprefix_injector
    from isotopic_logging.generators import generate_uuid_based_oid

    generator = generate_uuid_based_oid(12)

    with autoprefix_injector(oid_generator=generator) as inj:
        print(inj.mark("bar"))
        print(inj.mark("buz"))

    # Output:
    # "B2092A6EE743 | bar"
    # "B2092A6EE743 | buz"


Of course, you can define your own generator:

.. code-block:: python

    OID_LENGTH = 5
    OID_FORMAT = "{{0:>0{length}}}".format(length=OID_LENGTH)
    OID_MAX_VALUE = (10 ** OID_LENGTH) - 1

    def generate_oid():
        i = 0
        while True:
            yield OID_FORMAT.format(i)
            i = 0 if i == OID_MAX_VALUE else i + 1

    generator = generate_oid()

    with autoprefix_injector(oid_generator=generator) as inj:
        print(inj.mark("foo"))
        print(inj.mark("bar"))

    with autoprefix_injector(oid_generator=generator) as inj:
        print(inj.mark("buz"))

    # Output:
    # "00000 | foo"
    # "00000 | bar"
    # "00001 | buz"


If you do not want to bother yourself with passing generators each time, you
can use the power of partials:

.. code-block:: python

    from functools import partial

    custom_injector = partial(autoprefix_injector, oid_generator=generate_oid())

    with custom_injector() as inj:
        print(inj.mark("foo"))
        print(inj.mark("bar"))

    with custom_injector() as inj:
        print(inj.mark("buz"))

    # Output:
    # "00000 | foo"
    # "00000 | bar"
    # "00001 | buz"


Changelog
---------

* `1.1.0`_ (*pending*)

  * Feature: support nested prefixes (`issue #1`_).
  * Feature: simple and clean way to inject prefixes into calls to existing
    loggers (`issue #4`_).
  * Optimization: instances of injectors will be created only if new scope is
    defined (`issue #5`_).
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
.. _issue #4: https://github.com/oblalex/isotopic-logging/issues/4
.. _issue #5: https://github.com/oblalex/isotopic-logging/issues/5

.. _1.1.0: https://github.com/oblalex/isotopic-logging/compare/v1.0.1...v1.1.0
.. _1.0.1: https://github.com/oblalex/isotopic-logging/compare/v1.0.0...v1.0.1
.. _1.0.0: https://github.com/oblalex/isotopic-logging/releases/tag/v1.0.0
