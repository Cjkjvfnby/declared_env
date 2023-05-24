"""
Module declare a tools for working with env variables.

TODO write more info
https://realpython.com/python-descriptors/

"""
from abc import ABC
from logging import error

from declared_env._declared_variables import EnvironmentVariable
from declared_env._exceptions import DeclaredEnvironmentError, DeclaredEnvironmentExit
from declared_env._prefixable import Prefixable


class EnvironmentDeclaration(Prefixable, ABC):
    """
    Base class responsible for parsing environment.

    You need to declare an attribute `prefix: str` and add your variables declaration.
    Then you need to declare environment variables.
    Name of the attributes matter, expected environment variable names is constructed
    from the prefix underscore and class variable name, all in uppercase.

    >>> from declared_env._declared_variables import EnvironmentString
    >>> class MyEnv(EnvironmentDeclaration):
    ...     prefix = "FOO"
    ...     host = EnvironmentString(default="localhost")  # env: FOO_HOST
    ...
    >>> my_env = MyEnv()
    >>> my_env.host
    'localhost'
    """

    def __init__(self):
        """
        Initialize the parser.

        Environment lookups are done here.
        :raises: DeclaredEnvironmentExit in case of any error.
                 More detailed description is send to logging.error.
        """
        self.__settings = self.__get_settings()
        errors = self.validate()
        if errors == "never":
            msg = "This will never happen"
            raise ValueError(msg)
        if errors:
            err_text = "\n".join(str(e) for e in errors)
            error(f"Environment is not configured properly:\n{err_text}")
            raise DeclaredEnvironmentExit()

    def get_help(self) -> str:
        """
        Return help text for declared variables.

        TODO inject formatter
        """
        return "\n".join(s.get_help() for s in self.__settings)

    def validate(self) -> list[DeclaredEnvironmentError]:
        """Validate all variables and return error messages list."""
        errors = []

        for setting in self.__settings:
            try:
                setting.get_valid_value()
            except DeclaredEnvironmentError as e:
                errors.append(e)
        return errors

    def __get_settings(self) -> list[EnvironmentVariable]:
        return sorted(
            (
                v
                for v in self.__class__.__dict__.values()
                if isinstance(v, EnvironmentVariable)
            ),
            key=lambda x: x.name,
        )
