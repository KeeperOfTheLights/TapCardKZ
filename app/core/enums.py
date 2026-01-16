from enum import Enum   

class AssetType(Enum):
    avatar = "avatar"
    app_icon = "app_icon"

class Theme(Enum):
    light = "light"
    dark = "dark"

class SocialType(Enum):
    instagram = "instagram"
    telegram = "telegram"
    tiktok = "tiktok"
    youtube = "youtube"
    custom = "custom"
    
