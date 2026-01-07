from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum

from app.core.models.base import Base


class AssetType(PyEnum):
    avatar = "avatar"
    app_icon = "app_icon"

class CardAsset(Base):
    __tablename__ = "card_assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True)
    type: Mapped[AssetType] = mapped_column(SQLEnum(AssetType, name="asset_type"), nullable=False)
    file_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    card = relationship("Card", back_populates="assets")