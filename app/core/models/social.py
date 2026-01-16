from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base
from app.core import enums

class CardSocial(Base):
    __tablename__ = "card_socials"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True)
    type: Mapped[enums.SocialType] = mapped_column(SQLEnum(enums.SocialType, name="social_type"), nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    label: Mapped[str] = mapped_column(String, nullable=True)
    order_id: Mapped[int] = mapped_column(Integer)
    icon_asset_id: Mapped[int] = mapped_column(Integer, nullable=True)
    is_visible: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    card = relationship("Card", back_populates="socials")