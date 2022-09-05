"""Variables declarations."""
from __future__ import annotations

import os
from abc import ABCMeta, abstractmethod
from configparser import ConfigParser
from typing import Any, Optional, Type

from declared_env._exceptions import EnvironmentKeyError, EnvironmentValueError
from declared_env._prefixable import Prefixable


class EnvironmentVariable(metaclass=ABCMeta):
    """Base class for all environment variables."""

    @abstractmethod
    def converter(self, value: str) -> Any:
        """Convert value as string to variable raw type."""
        ...

    def __get__(self, obj: Prefixable, type_: Type = None):
        """
        Magic trick on first call replaces descriptor method with calculated value.

        See more about the descriptor protocol:
        https://docs.python.org/3/howto/descriptor.html#descriptor-protocol
        """
        val = self.get_valid_value()
        obj.__dict__[self.name] = val
        return obj.__dict__[self.name]

    def __set_name__(self, owner: Prefixable, name: str):
        """
        Save name of the assigned variable to the descriptor.

        See: https://docs.python.org/3/reference/datamodel.html#object.__set_name__
        """
        self.name = name
        self.var_name = f"{owner.prefix.upper()}_{name.upper()}"

    def __init__(
        self,
        required: bool = True,
        default: str = "",
        help_text: Optional[str] = None,
    ):
        """Initialize a descriptor with base fields."""
        self.help_text = help_text
        self.required = required
        # env variable must be a string
        self.default = default if default is None else str(default)

    def get_help(self) -> str:
        """
        Return a help string about a field.

        TODO: inject formatter
        """
        help_text = []
        if self.help_text:
            help_text.append(f"{self.help_text}")
        if self.required and not self.default:
            help_text.append("required")
        else:
            help_text.append(f"default={self.default}")
        help_message = ", ".join(help_text)
        return f"{self.var_name:<20}{help_message}"

    def __get_raw_value(self) -> str:
        """
        Return value from environment as string or default one as is.

        :raises: EnvironmentKeyError if value is not found.
        """
        val = os.getenv(self.var_name, self.default)
        if self.required and val is None:
            raise EnvironmentKeyError(self.var_name)
        return val

    def get_valid_value(self) -> Any:
        """
        Get value as desired type.

        Raises `EnvironmentValueError` error if value is not convertible to desired type.

        """
        val = self.__get_raw_value()
        try:
            return self.converter(val)
        except ValueError as e:
            raise EnvironmentValueError(str(e), self.var_name)

    def __str__(self):
        """Return string representation of the filed."""
        return f"{self.name}: {self.var_name}"


class EnvironmentString(EnvironmentVariable):
    """Represent an environment variable that is string."""

    def converter(self, value: str) -> Any:
        """Return string itself."""
        return value


class EnvironmentInteger(EnvironmentVariable):
    """Represent an environment variable that is integer."""

    def converter(self, value: str) -> Any:
        """Convert string representation to int."""
        return int(value)


class EnvironmentFloat(EnvironmentVariable):
    """Represent an environment variable that is float."""

    def converter(self, value: str) -> Any:
        """Convert string representation to float."""
        return float(value)


class EnvironmentBool(EnvironmentVariable):
    """Represent an environment variable that is True of False."""

    def converter(self, val: str) -> bool:
        """Convert string representation to boolean."""
        if val.lower() not in ConfigParser.BOOLEAN_STATES:
            raise EnvironmentValueError(f"Not a boolean: {val}", self.var_name)
        return ConfigParser.BOOLEAN_STATES[val.lower()]
