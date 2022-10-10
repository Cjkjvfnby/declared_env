"""Abstract class with prefix attribute."""
from abc import ABC, abstractmethod


class Prefixable(ABC):  # noqa: too-few-public-methods
    """Abstract class with prefix attribute."""

    @property
    @abstractmethod
    def prefix(self) -> str:
        """Prefix string."""
