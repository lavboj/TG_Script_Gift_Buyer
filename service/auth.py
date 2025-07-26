import logging
from telethon import TelegramClient, errors

from utils import log_config
from utils.error_wrapper import error_wrapper

log_config.setup_logging()

class ClientAuthenticator:
    def __init__(self, session_name: str, api_id: str, api_hash: str):
        self.session_name = session_name
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

    @error_wrapper(
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
    
    @error_wrapper(
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


"""
Модуль для аутентификации и управления подключением Telegram-клиента с использованием Telethon.

Содержит класс `ClientAuthenticator`, предназначенный для:
- подключения к Telegram с использованием `TelegramClient`,
- получения текущего пользователя в виде `InputPeer`
Функции обёрнуты в retry-механизм, который автоматически
повторяет запрос при определённых типах ошибок.

"""