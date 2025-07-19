import logging
from telethon import functions, errors
import asyncio

async def get_star_balance(client, peer) -> float:
    try:
        result = await client(functions.payments.GetStarsTransactionsRequest(
            peer=peer,
            offset='',
            limit=1
        ))
        stars = result.balance    
        return stars.amount + stars.nanos / 1e9
    
    except (errors.RPCError, ConnectionError, asyncio.TimeoutError) as e:
        logging.error(f"Failed to get star balance: {e}")
        raise

# Этот модуль отвечает за получение баланса звезд в Telegram через Telethon.
# Функция `get_star_balance` принимает объект клиента и возвращает баланс звезд
# в виде целого числа, учитывая как целую, так и дробную части.


        
    