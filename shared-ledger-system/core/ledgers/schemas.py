# core/ledgers/schemas.py
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict  # ConfigDict'i import et
from typing import Generic, TypeVar

T = TypeVar('T')

class LedgerEntryBase(BaseModel):
    operation: str
    amount: int = Field(..., description="Amount of credits for the operation")
    owner_id: str = Field(..., description="ID of the ledger owner")
    nonce: str = Field(..., description="Unique identifier for the transaction")

class LedgerEntryCreate(LedgerEntryBase):
    pass

class LedgerEntry(LedgerEntryBase):
    id: int
    created_on: datetime

    model_config = ConfigDict(from_attributes=True)  # class Config -> ConfigDict


class LedgerBalance(BaseModel):
    owner_id: str
    balance: int