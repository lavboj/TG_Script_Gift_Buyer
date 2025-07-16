from custom_tl.payments import GetStarGiftsRequest

def gift_parameters(gift) -> dict:
    return {
        "id": getattr(gift, "id", None),
        "price": getattr(gift, "stars", 0),
        "total": getattr(gift, "availability_total", 0),
        "left": getattr(gift, "sold_out", False),
        "availability": getattr(gift, "availability_remains", 0),
        "limited": getattr(gift, "limited", False)
    }

# Этот модуль содержит функцию gift_parameters, которая извлекает параметры подарка из объекта gift.
# Функция возвращает словарь с ключами, соответствующими различным атрибутам подарка

async def gift_filter(
        bot,
        min_price,
        max_price,
        min_supply,
        max_supply,
)-> list:
    
    api_gifts = await bot(GetStarGiftsRequest(hash=0))

    filtered_gifts = []
    for gift in api_gifts.gifts:
        params = gift_parameters(gift)

        price = params.get("price")
        sold_out = params.get("left")
        is_limited = params.get("limited")
        supply = params.get("availability")

        if not is_limited or sold_out:
            continue

        if min_price <= price <= max_price and min_supply <= supply <= max_supply:
            filtered_gifts.append(gift)

    return filtered_gifts

#Получаем список подарков и фильтруем их по заданным критериям
#Возвращаемый список содержит только те подарки, которые соответствуют условиям фильтрации.



    


        
