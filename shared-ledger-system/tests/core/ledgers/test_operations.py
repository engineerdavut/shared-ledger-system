# tests/core/ledgers/test_operations.py
import pytest
from enum import Enum
from core.ledgers.operations import LedgerOperationFactory


def test_ledger_operation_factory_creates_valid_enum():
    operations = {
        "DAILY_REWARD": "DAILY_REWARD",
        "SIGNUP_CREDIT": "SIGNUP_CREDIT",
        "CREDIT_SPEND": "CREDIT_SPEND",
        "CREDIT_ADD": "CREDIT_ADD",
        "CUSTOM_OP": "CUSTOM_OP",
    }

    enum_class = LedgerOperationFactory.create("TestOperation", operations)
    assert issubclass(enum_class, Enum)
    assert enum_class.DAILY_REWARD.value == "DAILY_REWARD"
    assert enum_class.CUSTOM_OP.value == "CUSTOM_OP"


def test_ledger_operation_factory_raises_error_on_missing_shared_ops():
    operations = {"CUSTOM_OP": "CUSTOM_OP"}

    with pytest.raises(ValueError):
        LedgerOperationFactory.create("TestOperation", operations)
