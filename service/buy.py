import logging
from telethon import functions, types, errors

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
async def buy_gift(client, peer, gift_id: int):
    invoice = types.InputInvoiceStarGift(peer=peer, gift_id=gift_id)
    
    payment_form = await client(functions.payments.GetPaymentFormRequest(invoice=invoice))
    logging.info(f"Form ID: {payment_form.form_id}")
    
    result = await client(functions.payments.SendStarsFormRequest(form_id=payment_form.form_id, invoice=invoice))
    logging.info(f"Подарок c ID {gift_id} успешно куплен.")

    return result

"""
Покупает подарок с заданным gift_id через Telegram Payments API.

Args:
    client: Telethon client (отправитель подарка).
    peer: Telegram peer (получатель подарка).
    gift_id (int): ID подарка.

Функция обёрнута в retry-механизм, который автоматически
повторяет запрос при определённых типах ошибок.

"""