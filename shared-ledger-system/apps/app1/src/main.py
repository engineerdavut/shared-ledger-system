# apps/app1/src/main.py
# apps/app1/src/main.py
from fastapi import FastAPI
from .api.core.ledgers.routes import router as ledger_router
import os  # os modülünü import et
from dotenv import load_dotenv
load_dotenv()

# Uygulama başlatılırken DATABASE_URL'yi kontrol et
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL or not DATABASE_URL.startswith("postgresql+asyncpg://"):
    raise ValueError("DATABASE_URL environment variable must be set and start with 'postgresql+asyncpg://'")

app = FastAPI()
app.include_router(ledger_router)
async def health_check():
    return {"status": "healthy"}