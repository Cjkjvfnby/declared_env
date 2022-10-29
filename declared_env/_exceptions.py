"""Custom exceptions."""
from typing import Any, Tuple


class DeclaredEnvironmentError(Exception):
    """Base exception for all raised errors."""

    def __init__(self, message: str, variable: Any, *args: Tuple[Any]):
        self.variable = variable
        super().__init__(message, *args)

    def __str__(self):
        """Return string representation of error."""
        return f"{self.variable}: {super().__str__()}"


class EnvironmentKeyError(DeclaredEnvironmentError):
    """Raised when a environment key is not found in the set of existing keys."""

    def __init__(self, variable: Any, *args: Tuple[Any]):
        self.variable = variable
        super().__init__("variable not set", variable, *args)


class EnvironmentValueError(DeclaredEnvironmentError):
    """Raised when an operation or function receives an argument that an inappropriate value."""


class DeclaredEnvironmentExit(DeclaredEnvironmentError, SystemExit):  # noqa: N818
    """
    Raised when validation of declared environment failed.

    That means that program is misconfigured and should exit with predefined status.
    """

    def __init__(self):
        super(SystemExit, self).__init__(88)
