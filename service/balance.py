from telethon import functions

async def get_star_balance(client) -> int:
    session = await client.get_me()
    peer = await client.get_input_entity(session)

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


        
    