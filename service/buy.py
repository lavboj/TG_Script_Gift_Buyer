import logging
from telethon import functions, types, errors
import asyncio

async def buy_gift(
    client,
    peer,
    gift_id: int,
):
    try:
        invoice=types.InputInvoiceStarGift(
                peer=peer,
                gift_id=gift_id
            )
        
        payment_form = await client(functions.payments.GetPaymentFormRequest(
            invoice=invoice
        ))
        logging.info(f"Form ID: {payment_form.form_id}")
        result = await client(functions.payments.SendStarsFormRequest(
            form_id=payment_form.form_id,
            invoice=invoice
        ))
        logging.info(f"Подарок c ID {gift_id} успешно куплен.")

    except (errors.RPCError, ConnectionError, asyncio.TimeoutError) as e:
        logging.error(f"Ошибка при покупке подарка c ID {gift_id}: {e}")
        raise

    return result