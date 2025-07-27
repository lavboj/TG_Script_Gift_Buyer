import asyncio
import logging
from telethon import errors

def error_wrapper(exceptions=()):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exceptions as e:
                if isinstance(e, errors.FloodWaitError):
                    logging.warning(f"Flood wait: waiting for {e.seconds} seconds")
                    await asyncio.sleep(e.seconds)
                else:
                    logging.error(f"Error while executing {func.__name__}: {e}")
                    raise RuntimeError(f"{func.__name__}")
            except Exception as e:
                logging.error(f"Unhandled exception while executing {func.__name__}: {e}")
                raise RuntimeError(f"{func.__name__}")
        return wrapper
    return decorator

"""
Модуль с реализацией error-декоратора для асинхронных функций.

Позволяет автоматически обрабатывать ошибки при возникновении указанных исключений,
в том числе с поддержкой обработки `FloodWaitError` от Telethon.

"""