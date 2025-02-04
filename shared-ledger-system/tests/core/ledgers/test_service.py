# tests/core/ledgers/test_service.py
import pytest
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from core.ledgers.service import LedgerService
from core.ledgers.schemas import LedgerEntryCreate
from core.ledgers.exceptions import InsufficientBalanceError, DuplicateTransactionError

@pytest.fixture
def ledger_service():
    config = {
        "DAILY_REWARD": 1,
        "SIGNUP_CREDIT": 3,
        "CREDIT_SPEND": -1,
        "CREDIT_ADD": 10,
    }
    return LedgerService(config)

@pytest.mark.asyncio
async def test_get_balance(ledger_service: LedgerService, async_session: AsyncSession):
    # Create some test entries
    entry1 = LedgerEntryCreate(
        operation="CREDIT_ADD",
        amount=10,
        owner_id="test_user",
        nonce="test1"
    )
    entry2 = LedgerEntryCreate(
        operation="CREDIT_SPEND",
        amount=-1,
        owner_id="test_user",
        nonce="test2"
    )
    
    await ledger_service.create_entry(async_session, entry1)
    await ledger_service.create_entry(async_session, entry2)
    
    balance = await ledger_service.get_balance(async_session, "test_user")
    assert balance == 9

@pytest.mark.asyncio
async def test_insufficient_balance(ledger_service: LedgerService, async_session: AsyncSession):
    entry = LedgerEntryCreate(
        operation="CREDIT_SPEND",
        amount=-10,
        owner_id="test_user",
        nonce="test3"
    )
    
    with pytest.raises(InsufficientBalanceError):
        await ledger_service.create_entry(async_session, entry)

@pytest.mark.asyncio
async def test_duplicate_nonce(ledger_service: LedgerService, async_session: AsyncSession):
    entry = LedgerEntryCreate(
        operation="CREDIT_ADD",
        amount=10,
        owner_id="test_user",
        nonce="test4"
    )
    
    await ledger_service.create_entry(async_session, entry)
    
    with pytest.raises(DuplicateTransactionError):
        await ledger_service.create_entry(async_session, entry)