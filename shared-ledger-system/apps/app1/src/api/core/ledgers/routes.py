# apps/app1/src/api/core/ledgers/routes.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.ledgers import service, schemas
from core.cache.cache import cache
from core.monitoring.prometheus import metrics
from core.logging.logger import logger
from core.auth import service as auth_service, models as auth_models
from .dependencies import rate_limit, get_redis_pool
from core.db.base import get_session
from core.config import core_settings
from core.ledgers.exceptions import InsufficientBalanceError, DuplicateTransactionError

router = APIRouter(prefix="/ledger", tags=["ledger"])


def get_ledger_service() -> service.LedgerService:
    return service.LedgerService(operation_config=core_settings.ledger.operation_config)


def get_ledger_cache():
    return cache


@router.get(
    "/{owner_id}",
    response_model=schemas.LedgerBalance,
    summary="Get Balance",
    description="Retrieves the current balance for a given owner.",
)
async def get_balance(
    request: Request,
    owner_id: str,
    session: AsyncSession = Depends(get_session),
    current_user: auth_models.User = Depends(auth_service.get_current_user),
    _: None = Depends(rate_limit),
    ledger_service: service.LedgerService = Depends(get_ledger_service),
    ledger_cache: cache = Depends(get_ledger_cache),
):
    cache_key = f"balance:{owner_id}"
    cached_balance = await ledger_cache.get_value(cache_key)
    if cached_balance is not None:
        metrics.cache_hit_count.labels(endpoint="get_balance").inc()
        return schemas.LedgerBalance(owner_id=owner_id, balance=int(cached_balance))

    metrics.cache_miss_count.labels(endpoint="get_balance").inc()
    try:
        with metrics.operation_duration_histogram.labels(
            operation_type="get_balance"
        ).time():
            balance = await ledger_service.get_balance(session, owner_id)
            await ledger_cache.set_value(
                cache_key, str(balance), ttl=core_settings.cache.default_ttl
            )
            metrics.balance_queries_counter.inc()

            logger.log_operation(
                operation_type="get_balance",
                user_id=current_user.id if current_user else "anonymous",
                details={
                    "owner_id": owner_id,
                    "balance": balance,
                    "request_id": request.headers.get("X-Request-ID"),
                },
            )
            return schemas.LedgerBalance(owner_id=owner_id, balance=balance)
    except Exception as e:
        logger.log_error(
            error_type="get_balance_error",
            user_id=current_user.id if current_user else "anonymous",
            error_details={
                "owner_id": owner_id,
                "error": str(e),
                "request_id": request.headers.get("X-Request-ID"),
            },
        )
        metrics.api_error_counter.labels(
            endpoint="get_balance", error_type=type(e).__name__
        ).inc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post(
    "/",
    response_model=dict,
    summary="Create Ledger Entry",
    description="Creates a new ledger entry for an owner.",
)
async def create_ledger_entry(
    request: Request,
    entry: schemas.LedgerEntryCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
    current_user: auth_models.User = Depends(auth_service.get_current_user),
    _: None = Depends(rate_limit),
    ledger_service: service.LedgerService = Depends(get_ledger_service),
    ledger_cache: cache = Depends(get_ledger_cache),
):
    try:
        with metrics.operation_duration_histogram.labels(
            operation_type="create_ledger_entry"
        ).time():
            result = await ledger_service.create_entry(session, entry)
            background_tasks.add_task(
                ledger_cache.invalidate_key, f"balance:{entry.owner_id}"
            )
            metrics.ledger_operations_counter.labels(
                operation_type="create_entry"
            ).inc()

            logger.log_operation(
                operation_type="create_ledger_entry",
                user_id=current_user.id if current_user else "anonymous",
                details={
                    "entry": entry.model_dump(),
                    "request_id": request.headers.get("X-Request-ID"),
                },
            )
            return {"status": "success", "message": "Ledger entry created successfully"}
    except InsufficientBalanceError as e:
        metrics.api_error_counter.labels(
            endpoint="create_ledger_entry", error_type="InsufficientBalanceError"
        ).inc()
        logger.log_error(
            error_type="insufficient_balance_error",
            user_id=current_user.id if current_user else "anonymous",
            error_details={
                "entry": entry.model_dump(),
                "error": str(e),
                "request_id": request.headers.get("X-Request-ID"),
            },
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DuplicateTransactionError as e:
        metrics.api_error_counter.labels(
            endpoint="create_ledger_entry", error_type="DuplicateTransactionError"
        ).inc()
        logger.log_error(
            error_type="duplicate_transaction_error",
            user_id=current_user.id if current_user else "anonymous",
            error_details={
                "entry": entry.model_dump(),
                "error": str(e),
                "request_id": request.headers.get("X-Request-ID"),
            },
        )
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e:
        metrics.api_error_counter.labels(
            endpoint="create_ledger_entry", error_type="ValueError"
        ).inc()
        logger.log_error(
            error_type="value_error",
            user_id=current_user.id if current_user else "anonymous",
            error_details={
                "entry": entry.model_dump(),
                "error": str(e),
                "request_id": request.headers.get("X-Request-ID"),
            },
        )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        metrics.api_error_counter.labels(
            endpoint="create_ledger_entry", error_type="ServerError"
        ).inc()
        logger.log_error(
            error_type="server_error",
            user_id=current_user.id if current_user else "anonymous",
            error_details={
                "entry": entry.model_dump(),
                "error": str(e),
                "request_id": request.headers.get("X-Request-ID"),
            },
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
