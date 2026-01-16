from pydantic import BaseModel, ConfigDict
from datetime import datetime       
from app.core import enums

class In(BaseModel):
    type: enums.SocialType
    url: str
    label: str

class Patch(BaseModel):
    type: enums.SocialType | None = None
    url: str | None = None
    label: str | None = None
    order_id: int | None = None
    icon_asset_id: int | None = None

class Base(BaseModel):
    id: int
    card_id: int
    type: enums.SocialType
    url: str
    label: str
    order_id: int
    icon_asset_id: int | None
    is_visible: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Out(Base):
    app_icon_link: str | None = None