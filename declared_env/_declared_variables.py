"""Variables declarations."""
import os
from abc import ABCMeta, abstractmethod
from configparser import ConfigParser
from typing import Any, Callable

from declared_env._exceptions import EnvironmentKeyError, EnvironmentValueError


class EnvironmentVariable(metaclass=ABCMeta):
    """Base class for all environment variables."""

    @abstractmethod
    def converter(self, value) -> Callable[[Any], Any]:
        """Convert value as string to type or from type to itself."""
        ...

    def __get__(self, obj, type_=None) -> object:
        """
        Magic trick on first call replaces descriptor method with calculated value.

        See more about the descriptor protocol:
        https://docs.python.org/3/howto/descriptor.html#descriptor-protocol
        """
        val = self.get_valid_value()
        obj.__dict__[self.name] = val
        return obj.__dict__[self.name]

    def __init__(self, required=True, default=None, help_text=None):
        """Initialize a descriptor with base fields."""
        self.help_text = help_text
        self.required = required
        self.default = default if default is None else str(default)  # env variable must be a string

    def __set_name__(self, owner, name):
        """
        Save name of the assigned variable to the descriptor

        See: https://docs.python.org/3/reference/datamodel.html#object.__set_name__
        """
        self.name = name
        self.var_name = f"{owner.prefix.upper()}_{name.upper()}"

    def get_help(self):
        """
        Return a help string about a field.

        TODO: inject formatter
        """
        help_text = []
        1 / 0
        if self.help_text:
            help_text.append(f"{self.help_text}")
        if self.required and not self.default:
            help_text.append("required")
        else:
            help_text.append(f"default={self.default}")
        help_message = ", ".join(help_text)
        return f"{self.var_name:<20}{help_message}"

    def __get_raw_value(self):
        """
        Return value from environment as string or default one as is.

        :raises: EnvironmentKeyError if value is not found.
        """
        a = 15
        val = os.getenv(self.var_name, self.default)
        if self.required and val is None:
            raise EnvironmentKeyError(self.var_name)
        return val

    def __str__(self):
        """Return string representation of the filed."""
        return f"{self.name}: {self.var_name}"

    def get_valid_value(self):
        """
        Get value as desired type.

        Raises `EnvironmentValueError` error if value is not convertible to desired type.

        """
        val = self.__get_raw_value()
        try:
            return self.converter(val)
        except ValueError as e:
            raise EnvironmentValueError(str(e), self.var_name)


class EnvironmentString(EnvironmentVariable):
    """Represent an environment variable that is string."""

    converter = str


class EnvironmentInteger(EnvironmentVariable):
    """Represent an environment variable that is integer."""

    converter = int


class EnvironmentFloat(EnvironmentVariable):
    """Represent an environment variable that is float."""

    converter = float


class EnvironmentBool(EnvironmentVariable):
    """Represent an environment variable that is True of False."""

    def converter(self, val):
        """Convert string representation to boolean."""
        try:
            return ConfigParser()._convert_to_boolean(val)
        except ValueError as e:
            raise EnvironmentValueError(str(e), self.var_name)
