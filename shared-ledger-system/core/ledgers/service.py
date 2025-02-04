# core/ledgers/service.py
from typing import Dict, Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from .models import LedgerEntry
from .schemas import LedgerEntryCreate
from .exceptions import InsufficientBalanceError, DuplicateTransactionError

class LedgerService:
    def __init__(self, operation_config: Dict[str, int]):
        self.operation_config = operation_config

    async def get_balance(self, session: AsyncSession, owner_id: str) -> int:
        """Get the current balance for an owner."""
        query = select(func.sum(LedgerEntry.amount)).where(LedgerEntry.owner_id == owner_id)
        result = await session.execute(query)
        balance = result.scalar() or 0
        return balance

    async def create_entry(
        self, 
        session: AsyncSession, 
        entry: LedgerEntryCreate
    ) -> LedgerEntry:
        """Create a new ledger entry with validation."""
        # Check for duplicate nonce
        existing = await session.execute(
            select(LedgerEntry).where(LedgerEntry.nonce == entry.nonce)
        )
        if existing.scalar_one_or_none():
            raise DuplicateTransactionError(f"Transaction with nonce {entry.nonce} already exists")

        # Get operation amount
        amount = self.operation_config.get(entry.operation)
        if amount is None:
            raise ValueError(f"Invalid operation: {entry.operation}")

        # Check balance for negative operations
        if amount < 0:
            current_balance = await self.get_balance(session, entry.owner_id)
            if current_balance + amount < 0:
                raise InsufficientBalanceError(
                    f"Insufficient balance: {current_balance} + {amount} < 0"
                )

        # Create entry
        db_entry = LedgerEntry(
            operation=entry.operation,
            amount=amount,
            nonce=entry.nonce,
            owner_id=entry.owner_id
        )
        session.add(db_entry)
        await session.commit()
        await session.refresh(db_entry)
        return db_entry