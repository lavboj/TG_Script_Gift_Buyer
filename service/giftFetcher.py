import auth
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

async def gift_filter(
        bot,
        min_price,
        max_price,
        min_supply,
        max_supply,
        unlimited,
):
    api_gifts = await bot(GetStarGiftsRequest(hash=0))
    


        
