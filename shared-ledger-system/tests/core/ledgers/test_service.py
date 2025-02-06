# tests/core/ledgers/test_service.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from core.ledgers.service import LedgerService
from core.ledgers.schemas import LedgerEntryCreate
from core.ledgers.exceptions import InsufficientBalanceError, DuplicateTransactionError
from core.ledgers.models import LedgerEntry
import uuid
from sqlalchemy import delete

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
    await async_session.execute(delete(LedgerEntry))
    await async_session.commit()
    # Create some test entries
    entry1 = LedgerEntryCreate(
        operation="CREDIT_ADD",
        owner_id="test_user",
        nonce=str(uuid.uuid4()),
        amount=10  # Gerekli, schemas.py'da zorunlu alan.
    )
    entry2 = LedgerEntryCreate(
        operation="CREDIT_SPEND",
        owner_id="test_user",
        nonce=str(uuid.uuid4()),
        amount=-1 # Gerekli, schemas.py'da zorunlu alan.
    )

    await ledger_service.create_entry(async_session, entry1)
    await ledger_service.create_entry(async_session, entry2)

    balance = await ledger_service.get_balance(async_session, "test_user")
    assert balance == 9  # (10) + (-1) = 9


@pytest.mark.asyncio
async def test_insufficient_balance(ledger_service: LedgerService, async_session: AsyncSession):
    await async_session.execute(delete(LedgerEntry))
    await async_session.commit()
    entry = LedgerEntryCreate(
        operation="CREDIT_SPEND",
        owner_id="test_user",
        nonce=str(uuid.uuid4()),
        amount=-1  # Gerekli
    )

    with pytest.raises(InsufficientBalanceError):
        await ledger_service.create_entry(async_session, entry)

@pytest.mark.asyncio
async def test_duplicate_nonce(ledger_service: LedgerService, async_session: AsyncSession):
    nonce = str(uuid.uuid4())
    entry = LedgerEntryCreate(
        operation="CREDIT_ADD",
        amount=10,  # amount zorunlu, herhangi bir değer olabilir
        owner_id="test_user",
        nonce=nonce
    )

    await ledger_service.create_entry(async_session, entry)

    duplicate_entry = LedgerEntryCreate(
        operation="CREDIT_ADD",
        amount=5,  # amount zorunlu, herhangi bir değer olabilir
        owner_id="test_user",
        nonce=nonce
    )

    with pytest.raises(DuplicateTransactionError):
        await ledger_service.create_entry(async_session, duplicate_entry)


@pytest.mark.asyncio
async def test_invalid_operation(ledger_service: LedgerService, async_session: AsyncSession):
    entry = LedgerEntryCreate(
        operation="INVALID_OPERATION",
        amount=10, # amount zorunlu
        owner_id="test_user",
        nonce=str(uuid.uuid4())
    )
    with pytest.raises(ValueError):
        await ledger_service.create_entry(async_session, entry)