from sqlalchemy import String, Boolean, ForeignKey, BigInteger, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base


class Theme(PyEnum):
    light = "light"
    dark = "dark"

class Setting(Base):
    __tablename__ = "settings"

    card_id: Mapped[int] = mapped_column(
        ForeignKey("cards.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    theme: Mapped[Theme] = mapped_column(
        SQLEnum(Theme, name="theme"),
        nullable=False,
        default=Theme.light
    )

    card: Mapped["Card"] = relationship("Card", back_populates="settings")