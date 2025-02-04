# core/ledgers/operations.py
from enum import Enum
from typing import Type, TypeVar, Dict
from abc import ABC, abstractmethod

class BaseLedgerOperation(ABC):
    """
    Abstract base class for ledger operations that enforces shared operations
    while allowing extensibility.
    """
    @classmethod
    @abstractmethod
    def get_shared_operations(cls) -> Dict[str, str]:
        """Returns the required shared operations."""
        return {
            "DAILY_REWARD": "DAILY_REWARD",
            "SIGNUP_CREDIT": "SIGNUP_CREDIT",
            "CREDIT_SPEND": "CREDIT_SPEND",
            "CREDIT_ADD": "CREDIT_ADD"
        }

    @classmethod
    def validate_operations(cls, enum_class: Type[Enum]) -> None:
        """Validates that an Enum class includes all required shared operations."""
        shared_ops = cls.get_shared_operations()
        enum_values = {item.value for item in enum_class}
        missing_ops = set(shared_ops.values()) - enum_values
        if missing_ops:
            raise ValueError(f"Missing required shared operations: {missing_ops}")

class LedgerOperationFactory:
    """
    Factory for creating ledger operation enums that enforce shared operations.
    """
    @staticmethod
    def create(name: str, operations: Dict[str, str]) -> Type[Enum]:
        """
        Creates an Enum class with the given operations, ensuring shared operations are included.
        """
        # Validate that all shared operations are included
        shared_ops = BaseLedgerOperation.get_shared_operations()
        for op in shared_ops.values():
            if op not in operations.values():
                raise ValueError(f"Missing required shared operation: {op}")

        # Create the Enum class
        return Enum(name, operations)