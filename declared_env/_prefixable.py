"""Abstract class with prefix attribute."""
from abc import ABCMeta, abstractmethod


class Prefixable(metaclass=ABCMeta):
    """Abstract class with prefix attribute."""

    @property
    @abstractmethod
    def prefix(self) -> str:
        """Prefix string."""
