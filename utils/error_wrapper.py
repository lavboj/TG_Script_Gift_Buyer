import asyncio
import logging
from telethon import errors

def error_wrapper(retry_exceptions=()):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except retry_exceptions as e:
                if isinstance(e, errors.FloodWaitError):
                    logging.warning(f"⏳ Flood wait: ждём {e.seconds} секунд")
                    await asyncio.sleep(e.seconds)
                else:
                    logging.error(f"Ошибка при выполнении {func.__name__}: {e}")
                    
                    raise RuntimeError(f"{func.__name__}")
            except Exception as e:
                logging.error(f"Необработанная ошибка при выполнении {func.__name__}: {e}")
                raise RuntimeError(f"{func.__name__}")
        return wrapper
    return decorator

"""
Модуль с реализацией error-декоратора для асинхронных функций.

Позволяет автоматически обрабатывать ошибки при возникновении указанных исключений,
в том числе с поддержкой обработки `FloodWaitError` от Telethon.

"""