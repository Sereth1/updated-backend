from sqlalchemy import Column, String, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    balances = relationship("WalletBalance", back_populates="wallet")


class WalletBalance(Base):
    __tablename__ = "wallet_balances"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wallet_id = Column(UUID(as_uuid=True), ForeignKey("wallets.id"), nullable=False)
    asset_id = Column(String, ForeignKey("assets.id"), nullable=False)
    balance = Column(Numeric, default=0)

    wallet = relationship("Wallet", back_populates="balances")
