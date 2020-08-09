import math

from pytest import mark, raises

from declared_env import (
    EnvironmentBool,
    EnvironmentDeclaration,
    EnvironmentFloat,
    EnvironmentInteger,
    EnvironmentString,
)

test_fields = [
    ("hello", EnvironmentString, "hello"),
    (42, EnvironmentInteger, 42),
    (3.14, EnvironmentFloat, 3.14),
    ("yes", EnvironmentBool, True),
]

test_data = test_fields + [
    (3, EnvironmentFloat, 3),
    ("inf", EnvironmentFloat, math.inf),
    ("NO", EnvironmentBool, False),
]


@mark.parametrize("value,field_class,expected", test_data)
def test_env_variable_is_returned(monkeypatch, value, field_class, expected):
    monkeypatch.setenv("FOO_VAR", str(value))

    class MyConfiguration(EnvironmentDeclaration):
        prefix = "FOO"
        var = field_class()

    my = MyConfiguration()
    assert my.var == expected


@mark.parametrize("default,field_class,expected", test_data)
def test_default_var(default, field_class, expected):
    class MyConfiguration(EnvironmentDeclaration):
        prefix = "FOO"
        var = field_class(default=default)

    my = MyConfiguration()
    assert my.var == expected


@mark.parametrize("default,field_class,expected", test_data)
def test_default_var_as_string(default, field_class, expected):
    class MyConfiguration(EnvironmentDeclaration):
        prefix = "FOO"
        var = field_class(default=str(default))

    my = MyConfiguration()
    assert my.var == expected


@mark.parametrize(
    "default,field_class,error_message",
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

    with raises(SystemExit):
        MyConfiguration()
    error_checker(error_message)


@mark.parametrize("default,field_class,expected", test_fields)
def test_help_with_default(default, field_class, expected):
    foo = field_class(default=default)

    class MyConfiguration(EnvironmentDeclaration):
        prefix = "FOO"
        var = foo

    help_text = foo.get_help()
    assert help_text == f"FOO_VAR             default={default}"


@mark.parametrize("default,field_class,expected", test_fields)
def test_help_with_required(default, field_class, expected):
    foo = field_class()

    class MyConfiguration(EnvironmentDeclaration):
        prefix = "FOO"
        var = foo

    help_text = foo.get_help()
    assert help_text == "FOO_VAR             required"


@mark.parametrize("default,field_class,expected", test_fields)
def test_help_with_required_and_help(default, field_class, expected):
    foo = field_class(help_text="help text")

    class MyConfiguration(EnvironmentDeclaration):
        prefix = "FOO"
        var = foo

    help_text = foo.get_help()
    assert help_text == "FOO_VAR             help text, required"


@mark.parametrize("default,field_class,expected", test_fields)
def test_help_with_default_and_help(default, field_class, expected):
    foo = field_class(help_text="help text", default=default)

    class MyConfiguration(EnvironmentDeclaration):
        prefix = "FOO"
        var = foo

    help_text = foo.get_help()
    assert help_text == f"FOO_VAR             help text, default={default}"
