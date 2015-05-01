# -*- coding: utf-8 -*-

from behave import given, when, then
from hamcrest import assert_that, equal_to, close_to
from six import string_types
from six.moves import range


from isotopic_logging.oid import default_oid_generator_class


@given("default generator with default parameters")
def step_impl(context):
    context.generator = default_oid_generator_class()


@given("default generator with length {length}")
def step_impl(context, length):
    context.generator = default_oid_generator_class(length=int(length))

@when("I ask for a single ID")
def step_impl(context):
    context.oid = context.generator()


@then("ID type must be string")
def step_impl(context):
    assert_that(isinstance(context.oid, string_types))


@then("ID length must be equal to {number}")
def step_impl(context, number):
    assert_that(len(context.oid), equal_to(int(number)))


@given("there are {number} different default generators")
def step_impl(context, number):
    context.generators = [
        default_oid_generator_class() for x in range(int(number))
    ]


@when("I ask each generator for an ID for {number} times")
def step_impl(context, number):
    context.results = []

    for generator in context.generators:
        context.results.extend([
            generator() for x in range(int(number))
        ])


@then("{percent}% of all generated IDs must be unique")
def step_impl(context, percent):
    total = len(context.results)
    unique = len(set(context.results))

    delta = total * (1 - float(percent) / 100)
    assert_that(unique, close_to(total, delta=delta))
