# apps/app1/src/main.py
from fastapi import FastAPI
from api.ledgers.routes import router as ledger_router

app = FastAPI(title="App1 Ledger API")

app.include_router(ledger_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}