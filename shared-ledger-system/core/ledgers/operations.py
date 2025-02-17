# core/ledgers/operations.py
from enum import Enum
from typing import Type, Dict
from abc import ABC, abstractmethod


class BaseLedgerOperation(ABC):
    @classmethod
    @abstractmethod
    def get_shared_operations(cls) -> Dict[str, str]:
        return {
            "DAILY_REWARD": "DAILY_REWARD",
            "SIGNUP_CREDIT": "SIGNUP_CREDIT",
            "CREDIT_SPEND": "CREDIT_SPEND",
            "CREDIT_ADD": "CREDIT_ADD",
        }

    @classmethod
    def validate_operations(cls, enum_class: Type[Enum]) -> None:
        shared_ops = cls.get_shared_operations()
        enum_values = {item.value for item in enum_class}
        missing_ops = set(shared_ops.values()) - enum_values
        if missing_ops:
            raise ValueError(f"Missing required shared operations: {missing_ops}")


class LedgerOperationFactory:
    @staticmethod
    def create(name: str, operations: Dict[str, str]) -> Type[Enum]:
        shared_ops = BaseLedgerOperation.get_shared_operations()
        for op in shared_ops.values():
            if op not in operations.values():
                raise ValueError(f"Missing required shared operation: {op}")
        return Enum(name, operations)
