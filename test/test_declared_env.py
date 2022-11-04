import pytest

from declared_env import (
    EnvironmentBool,
    EnvironmentDeclaration,
    EnvironmentFloat,
    EnvironmentInteger,
    EnvironmentString,
)


class MyConfiguration(EnvironmentDeclaration):
    prefix = "FOO"

    text_var = EnvironmentString()
    int_var = EnvironmentInteger()
    boolean_var = EnvironmentBool()
    float_var = EnvironmentFloat()


def test_env_variable_is_returned(monkeypatch):
    monkeypatch.setenv("FOO_TEXT_VAR", "text")
    monkeypatch.setenv("FOO_INT_VAR", "42")
    monkeypatch.setenv("FOO_BOOLEAN_VAR", "YES")
    monkeypatch.setenv("FOO_FLOAT_VAR", "3.14")

    configuration = MyConfiguration()
    assert configuration.int_var == 42
    assert configuration.text_var == "text"
    assert configuration.boolean_var is True
    assert configuration.float_var == pytest.approx(3.14)


def test_missing_var(error_checker):
    with pytest.raises(SystemExit):
        MyConfiguration()
    error_checker(
        "FOO_BOOLEAN_VAR: variable not set",
        "FOO_FLOAT_VAR: variable not set",
        "FOO_INT_VAR: variable not set",
        "FOO_TEXT_VAR: variable not set",
    )


def test_help():
    class ForHelp(EnvironmentDeclaration):
        prefix = "FOO"

        text_var = EnvironmentString(default="text", help_text="a text")
        int_var = EnvironmentInteger(default=42, help_text="a int")
        boolean_var = EnvironmentBool(default=True, help_text="a bool")
        float_var = EnvironmentFloat(default=3.15, help_text="a float")

    for_help = ForHelp()
    help_string = for_help.get_help()
    expected = "\n".join(
        [
            "FOO_BOOLEAN_VAR     a bool, default=True",
            "FOO_FLOAT_VAR       a float, default=3.15",
            "FOO_INT_VAR         a int, default=42",
            "FOO_TEXT_VAR        a text, default=text",
        ],
    )

    assert help_string == expected
