# apps/app1/src/api/ledgers/schemas.py
from enum import Enum
from core.ledgers.operations import LedgerOperationFactory

# App1'e özel ledger operasyonları
APP1_OPERATIONS = {
    "DAILY_REWARD": "DAILY_REWARD",
    "SIGNUP_CREDIT": "SIGNUP_CREDIT",
    "CREDIT_SPEND": "CREDIT_SPEND",
    "CREDIT_ADD": "CREDIT_ADD",
    "CONTENT_CREATION": "CONTENT_CREATION",
    "CONTENT_ACCESS": "CONTENT_ACCESS"
}

# Factory kullanarak Enum oluştur
App1LedgerOperation = LedgerOperationFactory.create("App1LedgerOperation", APP1_OPERATIONS)

# Operasyon konfigürasyonu
APP1_LEDGER_OPERATION_CONFIG = {
    "DAILY_REWARD": 1,
    "SIGNUP_CREDIT": 3,
    "CREDIT_SPEND": -1,
    "CREDIT_ADD": 10,
    "CONTENT_CREATION": -5,
    "CONTENT_ACCESS": 0,
}