# core/ledgers/models.py
from datetime import datetime
import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAlchemyEnum
from core.db.base import Base


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"

    id = Column(Integer, primary_key=True)
    operation = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    nonce = Column(String, nullable=False, unique=True)
    owner_id = Column(String, nullable=False)
    created_on = Column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        sqlalchemy.Index("idx_owner_id", "owner_id"),
        sqlalchemy.Index("idx_nonce", "nonce"),
    )
