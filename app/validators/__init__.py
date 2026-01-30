"""
Validators module for Taply API.

Contains validation layer that separates HTTP errors from business logic.
Validators are called from routers before services.

Modules:
    - cards: Card existence checks
    - socials: Social link and icon checks
    - codes: Activation code checks
    - assets: Image file validation
    - auth: JWT token verification

Usage example:
    ```python
    from app import validators
    
    # In router (before calling service):
    card = await validators.cards.require_card(card_id=1, session=session)
    validators.assets.validate_image(file)
    
    # Then call service with validated data:
    result = await services.cards.get(card=card, ...)
    ```
"""
from app.validators import cards, socials, codes, assets, auth

__all__ = ["cards", "socials", "codes", "assets", "auth"]
