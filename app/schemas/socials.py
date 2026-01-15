from pydantic import BaseModel, ConfigDict
from datetime import datetime       
from app.core.models.social import SocialType

class SocialIn(BaseModel):
    type: SocialType
    url: str
    label: str

class SocialPatch(BaseModel):
    type: SocialType | None = None
    url: str | None = None
    label: str | None = None
    order_id: int | None = None
    icon_asset_id: int | None = None

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

class SocialOut(BaseSocial):
    app_icon_link: str | None = None