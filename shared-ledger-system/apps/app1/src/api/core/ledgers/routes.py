# apps/app1/src/api/ledgers/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.ledgers.schemas import LedgerEntryCreate, LedgerBalance
from core.ledgers.service import LedgerService
from core.ledgers.exceptions import InsufficientBalanceError, DuplicateTransactionError
from core.db.base import get_session
from .schemas import APP1_LEDGER_OPERATION_CONFIG

router = APIRouter(prefix="/ledger", tags=["ledger"])
ledger_service = LedgerService(APP1_LEDGER_OPERATION_CONFIG)

@router.get("/{owner_id}", response_model=LedgerBalance)
async def get_balance(
    owner_id: str,
    session: AsyncSession = Depends(get_session)
) -> LedgerBalance:
    """Get current balance for an owner."""
    try:
        balance = await ledger_service.get_balance(session, owner_id)
        return LedgerBalance(owner_id=owner_id, balance=balance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=dict)
async def create_ledger_entry(
    entry: LedgerEntryCreate,
    session: AsyncSession = Depends(get_session)
) -> dict:
    """Create a new ledger entry."""
    try:
        await ledger_service.create_entry(session, entry)
        return {"status": "success", "message": "Ledger entry created successfully"}
    except InsufficientBalanceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DuplicateTransactionError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))