# apps/app1/src/main.py
from fastapi import FastAPI, Request, HTTPException
from starlette.responses import JSONResponse
from .api.core.ledgers.routes import router as ledger_router
from core.monitoring.prometheus import metrics
from core.logging.logger import logger
from core.auth.routes import router as auth_router
from core.config import core_settings
from .config import app1_settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import OperationalError
import time

app = FastAPI(title=core_settings.app_name, debug=core_settings.debug)

if core_settings.prometheus.prometheus_enabled:
    metrics.init_app(app)
else:
    logger.logger.info("Prometheus metrics are disabled.")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.logger.info(
        f"Request: {request.method} {request.url} - Client: {request.client.host if request.client else 'N/A'}"
    )
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.logger.info(
        f"Response status code: {response.status_code} - Endpoint: {request.url.path} - Time: {process_time:.4f}s"
    )
    return response


app.include_router(ledger_router)
app.include_router(auth_router)


@app.get("/healthz", tags=["health"])
async def health_check():
    try:
        engine = create_async_engine(core_settings.database.database_url)
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        return {
            "status": "healthy",
            "app_name": core_settings.app_name,
            "version": "0.1.0",
        }
    except OperationalError:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": "Database connection failed"},
        )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.logger.warning(
        f"HTTPException: {exc.status_code} - {exc.detail} - Endpoint: {request.url.path} - Method: {request.method}"
    )
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.logger.error(
        f"Global exception: {exc} - Endpoint: {request.url.path}", exc_info=True
    )
    return JSONResponse(status_code=500, content={"message": "Internal Server Error"})


logger.logger.info(
    f"Application '{core_settings.app_name}' started - "
    f"Log Level: {core_settings.logging.log_level}, "
    f"Prometheus: {'enabled' if core_settings.prometheus.prometheus_enabled else 'disabled'}"
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=core_settings.debug,
        workers=4 if not core_settings.debug else 1,
    )
