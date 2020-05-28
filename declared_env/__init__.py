"""
Declared environment.

This package will help you to:
  - declare you environment expectation
  - check presence of all required variables (with meaningful errors)
  - list your variables for documentation purposes
"""

from declared_env._declared_variables import (
    EnvironmentBool,
    EnvironmentFloat,
    EnvironmentInteger,
    EnvironmentString,
)
from declared_env._environment_parser import EnvironmentDeclaration

__version__ = "1.0.0"
