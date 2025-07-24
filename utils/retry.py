import asyncio
import logging
from telethon import errors

def make_retry_wrapper(max_retries=3, delay=1, retry_exceptions=()):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except retry_exceptions as e:
                    if isinstance(e, errors.FloodWaitError):
                        logging.warning(f"⏳ Flood wait: ждём {e.seconds} секунд (попытка {attempt + 1}/{max_retries})")
                        await asyncio.sleep(e.seconds)
                    else:
                        logging.error(f"Ошибка при выполнении {func.__name__}: {e} (попытка {attempt + 1}/{max_retries})")
                        await asyncio.sleep(delay)
                except Exception as e:
                    logging.error(f"Необработанная ошибка при выполнении {func.__name__}: {e}")
                    raise

            logging.critical(f"Максимальное количество попыток ({max_retries}) исчерпано для {func.__name__}")
            raise RuntimeError(f"Максимальное количество попыток ({max_retries}) исчерпано для {func.__name__}")
        return wrapper
    return decorator

"""
Модуль с реализацией retry-декоратора для асинхронных функций.

Позволяет автоматически повторять выполнение функции при возникновении указанных исключений,
в том числе с поддержкой обработки `FloodWaitError` от Telethon.

"""