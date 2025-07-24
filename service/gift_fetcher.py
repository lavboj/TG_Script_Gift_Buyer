import logging
from telethon import functions, errors

from utils.retry import make_retry_wrapper

def gift_parameters(gift) -> dict:
    return {
        "id": getattr(gift, "id", None),
        "price": getattr(gift, "stars", 0) or 0,
        "total": getattr(gift, "availability_total", 0),
        "sold_out": getattr(gift, "sold_out", False),
        "availability": getattr(gift, "availability_remains", 0) or 0,
        "limited": getattr(gift, "limited", False)
    }

@make_retry_wrapper(
    max_retries=3,
    delay=1,
    retry_exceptions=(
        errors.FloodWaitError,
        errors.ServerError,
        errors.TimeoutError,
        ConnectionError,
        errors.RPCError
    )
)
async def gift_filter(
        client,
        min_price,
        max_price,
        max_supply
)-> list:
    
    api_gifts = await client(functions.payments.GetStarGiftsRequest(hash=0))

    filtered_gifts = []

    for gift in api_gifts.gifts:
        try:
            params = gift_parameters(gift)

            price = params.get("price")
            sold_out = params.get("sold_out")
            is_limited = params.get("limited")
            total = params.get("total")

            if not is_limited or sold_out:
                continue

            if min_price <= price <= max_price and total <= max_supply:
                filtered_gifts.append(params)
        except Exception as e:
            logging.error(f"Ошибка при обработке подарка: {e}")
            continue

    return filtered_gifts

"""
Модуль для фильтрации подарков (gifts) на основе цен и ограничений по доступности.

Содержит:
- Функцию `gift_parameters`, которая извлекает и нормализует параметры из объекта подарка.
- Асинхронную функцию `gift_filter`, которая обращается к Telegram API через Telethon
  и фильтрует список подарков по заданным критериям.

Функция обёрнута в retry-механизм, который автоматически
повторяет запрос при определённых типах ошибок.

"""




        
