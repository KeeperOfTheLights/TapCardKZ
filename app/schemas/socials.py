from pydantic import BaseModel, ConfigDict
from datetime import datetime       
from app.core.models.social import SocialType

class BaseSocial(BaseModel):
    id: int
    card_id: int
    type: SocialType
    url: str
    label: str
    order_id: int
    icon_asset_id: int | None
    is_visible: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SocialPatch(BaseSocial):
    type: SocialType | None = None
    url: str | None = None
    label: str | None = None
    order_id: int | None = None
    icon_asset_id: int | None = None