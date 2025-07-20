import logging
from telethon import functions

def gift_parameters(gift) -> dict:
    return {
        "id": getattr(gift, "id", None),
        "price": getattr(gift, "stars", 0) or 0,
        "total": getattr(gift, "availability_total", 0),
        "sold_out": getattr(gift, "sold_out", False),
        "availability": getattr(gift, "availability_remains", 0) or 0,
        "limited": getattr(gift, "limited", False)
    }

# Этот модуль содержит функцию gift_parameters, которая извлекает параметры подарка из объекта gift.
# Функция возвращает словарь с ключами, соответствующими различным атрибутам подарка

async def gift_filter(
        client,
        min_price,
        max_price,
        max_supply
)-> list:
    
    try:
        api_gifts = await client(functions.payments.GetStarGiftsRequest(hash=0))
    except Exception as e:
        logging.error(f"Ошибка при получении подарков: {e}")
        return []

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

#Получаем список подарков и фильтруем их по заданным критериям
#Возвращаемый список содержит только те подарки, которые соответствуют условиям фильтрации.






        
