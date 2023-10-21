import math

import pytest

from declared_env import (
    EnvironmentBool,
    EnvironmentDeclaration,
    EnvironmentFloat,
    EnvironmentInteger,
    EnvironmentString,
)


def init_field(field):
    class MyConfiguration(EnvironmentDeclaration):  # pylint: disable=unused-variable
        prefix = "FOO"
        var = field


test_fields = [
    ("hello", EnvironmentString, "hello"),
    (42, EnvironmentInteger, 42),
    (3.14, EnvironmentFloat, 3.14),
    ("yes", EnvironmentBool, True),
]

test_data = [
    *test_fields,
    (3, EnvironmentFloat, 3),
    ("inf", EnvironmentFloat, math.inf),
    ("NO", EnvironmentBool, False),
]


@pytest.mark.parametrize(("value", "field_class", "expected"), test_data)
def test_env_variable_is_returned(monkeypatch, value, field_class, expected):
    monkeypatch.setenv("FOO_VAR", str(value))

    class MyConfiguration(EnvironmentDeclaration):
        prefix = "FOO"
        var = field_class()

    configuration = MyConfiguration()
    assert configuration.var == expected


@pytest.mark.parametrize(("default", "field_class", "expected"), test_data)
def test_default_var(default, field_class, expected):
    class MyConfiguration(EnvironmentDeclaration):
        prefix = "FOO"
        var = field_class(default=default)

    configuration = MyConfiguration()
    assert configuration.var == expected


@pytest.mark.parametrize(("default", "field_class", "expected"), test_data)
def test_default_var_as_string(default, field_class, expected):
    class MyConfiguration(EnvironmentDeclaration):
        prefix = "FOO"
        var = field_class(default=str(default))

    configuration = MyConfiguration()
    assert configuration.var == expected


@pytest.mark.parametrize(
    ("default", "field_class", "error_message"),
    [
        (
            "hello",
            EnvironmentInteger,
            "FOO_VAR: invalid literal for int() with base 10: 'hello'",
        ),
        (
            "hello",
            EnvironmentFloat,
            "FOO_VAR: could not convert string to float: 'hello'",
        ),
        ("hello", EnvironmentBool, "FOO_VAR: Not a boolean: hello"),
    ],
)
def test_invalid(default, field_class, error_message, error_checker):
    class MyConfiguration(EnvironmentDeclaration):
        prefix = "FOO"
        var = field_class(default=default)

    with pytest.raises(SystemExit):
        MyConfiguration()
    error_checker(error_message)


@pytest.mark.parametrize(
    ("default", "field_class"),
    [(default, fk) for default, fk, _ in test_fields],
)
def test_help_with_default(default, field_class):
    field = field_class(default=default)
    init_field(field)
    help_text = field.get_help()
    assert help_text == f"FOO_VAR             default={default}"


@pytest.mark.parametrize("field_class", [fk for _, fk, _ in test_fields])
def test_help_with_required(field_class):
    field = field_class()
    init_field(field)
    help_text = field.get_help()
    assert help_text == "FOO_VAR             required"


@pytest.mark.parametrize("field_class", [fk for _, fk, _ in test_fields])
def test_help_with_required_and_help(field_class):
    field = field_class(help_text="help text")
    init_field(field)
    help_text = field.get_help()
    assert help_text == "FOO_VAR             help text, required"


@pytest.mark.parametrize(
    ("default", "field_class"),
    [(default, fk) for default, fk, _ in test_fields],
)
def test_help_with_default_and_help(default, field_class):
    field = field_class(help_text="help text", default=default)
    init_field(field)
    help_text = field.get_help()
    assert help_text == f"FOO_VAR             help text, default={default}"
