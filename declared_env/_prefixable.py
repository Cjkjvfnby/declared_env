"""Abstract class with prefix attribute."""
from abc import ABC, abstractmethod


class Prefixable(ABC):  # noqa: PLR0903
    """Abstract class with prefix attribute."""

    @property
    @abstractmethod
    def prefix(self) -> str:
        """Prefix string."""
