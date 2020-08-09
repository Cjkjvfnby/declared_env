"""
Module declare a tools for working with env variables.

TODO write more info
https://realpython.com/python-descriptors/

"""
from abc import ABCMeta, abstractmethod
from logging import error
from typing import List

from declared_env._declared_variables import EnvironmentString, EnvironmentVariable
from declared_env._exceptions import (
    DeclaredEnvironmentException,
    DeclaredEnvironmentExit,
)


class EnvironmentDeclaration(metaclass=ABCMeta):
    """
    Base class responsible for parsing environment.

    You need to declare an attribute `prefix: str` and add your variables declaration.
    Then you need to declare environment variables.
    Name of the variables matter, expected environmentvatraible name is constructed
    from the prefix underscore and class variable name, all in uppercase.

    >>> class MyEnv(EnvironmentDeclaration):
    ...     prefix = "FOO"
    ...     host = EnvironmentString(default="localhost")  # env: FOO_HOST
    ...
    >>> my_env = MyEnv()
    >>> my_env.host
    'localhost'
    """

    @property
    @abstractmethod
    def prefix(self) -> str:
        """Prefix for environment variable name."""
        ...

    def __init__(self):
        """
        Initialize the parser.

        Environment lookups are done here.
        :raises: DeclaredEnvironmentExit in case of any error.
                 More detailed description is send to logging.error.
        """
        self.__settings = self.__get_settings()
        errors = self.validate()
        if errors:
            err_text = "\n".join(str(e) for e in errors)
            error(f"Environment is not configured properly:\n{err_text}")
            raise DeclaredEnvironmentExit()

    def get_help(self):
        """
        Return help text for declared variables.

        TODO inject formatter
        """
        return "\n".join(s.get_help() for s in self.__settings)

    def validate(self) -> List[DeclaredEnvironmentException]:
        """Validate all variables and return error messages list."""
        errors = []

        for s in self.__settings:
            try:
                s.get_valid_value()
            except DeclaredEnvironmentException as e:
                errors.append(e)
        return errors

    def __get_settings(self):
        return sorted(
            (
                v
                for v in self.__class__.__dict__.values()
                if isinstance(v, EnvironmentVariable)
            ),
            key=lambda x: x.name,
        )
