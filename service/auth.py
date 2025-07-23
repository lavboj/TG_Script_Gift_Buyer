import logging
from telethon import TelegramClient, errors

from utils import log_config
from utils.retry import make_retry_wrapper

log_config.setup_logging()

class ClientAuthenticator:
    def __init__(self, session_name: str, api_id: str, api_hash: str):
        self.session_name = session_name
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

    @make_retry_wrapper(
        max_retries=5,
        delay=2,
        retry_exceptions=(
            errors.FloodWaitError,
            errors.ServerError,
            errors.TimeoutError,
            ConnectionError,
            errors.RPCError
        )
    )
    async def connect(self):
        await self.client.start()
        logging.info("Client connected successfully.")
        return self.client
    
    @make_retry_wrapper(
        max_retries=5,
        delay=2,
        retry_exceptions=(
            errors.FloodWaitError,
            errors.ServerError,
            errors.TimeoutError,
            ConnectionError,
            errors.RPCError
        )
    )
    async def get_input_peer(self):
        session = await self.client.get_me()
        peer = await self.client.get_input_entity(session)
        logging.info("Peer created successfully.")
        return peer
    
    async def disconnect(self):
        if self.client.is_connected():
            try:
                await self.client.disconnect()
                logging.info("Client disconnected successfully.")
            except Exception as e:
                logging.error(f"Error during client disconnection: {e}")


# Этот модуль отвечает за аутентификацию клиента в Telegram через Telethon.

# Класс ClientAuthenticator инициализирует клиента с API ID, API HASH,
# а затем запускает процесс авторизации и сохраняет сессию.

# Метод `connect` — асинхронный, запускает клиент и возвращает
# готовый к работе объект TelegramClient.