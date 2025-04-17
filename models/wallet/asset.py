from sqlalchemy import Column, String
from database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(String, primary_key=True)       # e.g. 'btc', 'eur'
    symbol = Column(String, nullable=False)     # e.g. 'BTC'
    name = Column(String, nullable=False)       # e.g. 'Bitcoin'
    type = Column(String, nullable=False)       # 'crypto' or 'fiat'
