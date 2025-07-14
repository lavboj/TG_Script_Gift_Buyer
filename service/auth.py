from telethon.sync import TelegramClient

class BotAuthenticator:
    def __init__(self, session_name: str, api_id: str, api_hash: str, bot_token: str):
        self.session_name = session_name
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)

    async def connect(self):
        await self.client.start(bot_token=self.bot_token)
        return self.client


# Этот модуль отвечает за аутентификацию бота в Telegram через Telethon.
# Класс BotAuthenticator инициализирует клиента с API ID, API HASH и токеном бота,
# а затем запускает процесс авторизации и сохраняет сессию.

# Метод `connect` — асинхронный, запускает клиент с бот-токеном и возвращает
# готовый к работе объект TelegramClient.