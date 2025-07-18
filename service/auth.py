from telethon.sync import TelegramClient

class ClientAuthenticator:
    def __init__(self, session_name: str, api_id: str, api_hash: str):
        self.session_name = session_name
        self.api_id = api_id
        self.api_hash = api_hash
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

    async def connect(self):
        await self.client.start()
        return self.client


# Этот модуль отвечает за аутентификацию клиента в Telegram через Telethon.

# Класс ClientAuthenticator инициализирует клиента с API ID, API HASH,
# а затем запускает процесс авторизации и сохраняет сессию.

# Метод `connect` — асинхронный, запускает клиент и возвращает
# готовый к работе объект TelegramClient.