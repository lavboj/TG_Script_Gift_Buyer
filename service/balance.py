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

"""
Модуль для получения баланса звёзд (stars) пользователя через Telethon.

Этот модуль содержит функцию `get_star_balance`, которая асинхронно обращается к API Telegram
через метод `payments.GetStarsTransactionsRequest`, чтобы получить текущий баланс звёзд
у заданного пользователя (peer). Функция обёрнута в retry-механизм, который автоматически
повторяет запрос при определённых типах ошибок.

"""
        
    