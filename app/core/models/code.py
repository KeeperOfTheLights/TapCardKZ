from datetime import datetime
from sqlalchemy import String, Boolean, ForeignKey, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base

class Code(Base):
    __tablename__ = "codes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True)
    code_hash: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    card = relationship("Card", back_populates="codes")
