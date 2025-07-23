from telethon import functions, errors

from utils.retry import make_retry_wrapper

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
async def get_star_balance(client, peer) -> float:
    result = await client(functions.payments.GetStarsTransactionsRequest(
        peer=peer,
        offset='',
        limit=1
    ))
    stars = result.balance    
    return stars.amount + stars.nanos / 1e9

# Этот модуль отвечает за получение баланса звезд в Telegram через Telethon.
# Функция `get_star_balance` принимает объект клиента и возвращает баланс звезд
# в виде целого числа, учитывая как целую, так и дробную части.


        
    