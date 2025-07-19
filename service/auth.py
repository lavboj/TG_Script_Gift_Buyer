import logging
from telethon import TelegramClient, errors
import asyncio

from utils import log_config

log_config.setup_logging()

class ClientAuthenticator:
    def __init__(self, session_name: str, api_id: str, api_hash: str):
        self.session_name = session_name
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

    async def connect(self, retries: int = 3, delay: int = 5):
        for attempt in range(1, retries + 1):
            try:
                await self.client.start()
                logging.info("Client connected successfully.")
                return self.client
            except (errors.RPCError, ConnectionError, asyncio.TimeoutError) as e:
                logging.warning(f"Connection attempt {attempt}/{retries} failed: {e}")
                if attempt < retries:
                    await asyncio.sleep(delay)
                else:
                    logging.critical("Failed to connect after multiple attempts.")
                    raise
    
    async def get_input_peer(self):
        try:
            session = await self.client.get_me()
            peer = await self.client.get_input_entity(session)
            return peer
        except (errors.RPCError, ConnectionError, asyncio.TimeoutError) as e:
            logging.error(f"Failed to get input peer: {e}")
            raise


# Этот модуль отвечает за аутентификацию клиента в Telegram через Telethon.

# Класс ClientAuthenticator инициализирует клиента с API ID, API HASH,
# а затем запускает процесс авторизации и сохраняет сессию.

# Метод `connect` — асинхронный, запускает клиент и возвращает
# готовый к работе объект TelegramClient.