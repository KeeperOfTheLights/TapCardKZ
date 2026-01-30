"""
Модуль валидаторов для Taply API.

Содержит слой проверок, который отделяет HTTP-ошибки от бизнес-логики.
Валидаторы вызываются из роутеров перед сервисами.

Модули:
    - cards: Проверка существования карточек
    - socials: Проверка социальных сетей и иконок
    - codes: Проверка кодов активации
    - assets: Валидация загружаемых изображений
    - auth: Проверка JWT токенов

Пример использования:
    ```python
    from app import validators
    
    # В роутере (до вызова сервиса):
    card = await validators.cards.require_card(card_id=1, session=session)
    validators.assets.validate_image(file)
    
    # Затем вызов сервиса с провалидированными данными:
    result = await services.cards.get(card=card, ...)
    ```
"""
from app.validators import cards, socials, codes, assets, auth

__all__ = ["cards", "socials", "codes", "assets", "auth"]
