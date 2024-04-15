"""Abstract class with prefix attribute."""

from abc import ABC, abstractmethod


class Prefixable(ABC):
    """Abstract class with prefix attribute."""

    @property
    @abstractmethod
    def prefix(self) -> str:
        """Prefix string."""
