# apps/app1/src/api/ledgers/schemas.py
from enum import Enum
from core.ledgers.operations import LedgerOperationFactory, BaseLedgerOperation

app1_specific_operations_definitions = {
    "CONTENT_CREATION": "CONTENT_CREATION",
    "CONTENT_ACCESS": "CONTENT_ACCESS",
}

shared_operations_definitions = BaseLedgerOperation.get_shared_operations()

app1_operations_definitions = {
    **shared_operations_definitions,
    **app1_specific_operations_definitions,
}

App1LedgerOperation: Enum = LedgerOperationFactory.create(
    "App1LedgerOperation", app1_operations_definitions
)

app1_ledger_operation_configuration = {
    App1LedgerOperation.DAILY_REWARD: 1,
    App1LedgerOperation.SIGNUP_CREDIT: 3,
    App1LedgerOperation.CREDIT_SPEND: -1,
    App1LedgerOperation.CREDIT_ADD: 10,
    App1LedgerOperation.CONTENT_CREATION: -5,
    App1LedgerOperation.CONTENT_ACCESS: 0,
}

APP1_LEDGER_OPERATION_CONFIG = app1_ledger_operation_configuration
APP1_OPERATIONS_ENUM = App1LedgerOperation
