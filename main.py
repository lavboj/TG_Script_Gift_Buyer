# Стандартные библиотеки
import logging
import asyncio
import os
import sys
import json

# Сторонние библиотеки
from dotenv import load_dotenv

# Локальные модули/пакеты
from service.balance import get_star_balance
from service.buy import buy_gift
from service import gift_fetcher, auth
from utils import log_config

log_config.setup_logging(level=logging.DEBUG) 

async def start_script(api_id, api_hash, channel_name, config):
    client = None

    min_price = config.get('min_price', 200)
    max_price = config.get('max_price', 2000)
    max_supply = config.get('max_supply', 250000)

    try:
        #Создание клиента и подключение к Telegram
        auth_client = auth.ClientAuthenticator('authClient', api_id, api_hash)
        client = await auth_client.connect()

        #Создание peer канала и peer пользователя
        channel_peer = await client.get_input_entity(channel_name)
        peer = await auth_client.get_input_peer()
    
        logging.info("Сканируем подарки...")

        #Основной цикл который вводит скрипт в сканирование подарков и их покупку
        while True:
            # Получение списка подарков по заданным параметрам
            if not client.is_connected():
                logging.critical("Reconnection failed")
                sys.exit(1)
            try:
                gift_list = await gift_fetcher.gift_filter(client, min_price, max_price, max_supply)
                balance = await get_star_balance(client, peer)
            except RuntimeError as e:
                logging.error(f"Error: {e}")
                continue
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                continue

            # Если есть подарки, начинаем их покупку опираясь на текущий баланс
            if balance < 200:
                logging.info("Деньги кончились, отключаемся...")
                break

            if gift_list:
                for gift in gift_list:
                    if balance < 200:
                        break
                    try:
                        await buy_gift(client, channel_peer, gift['id'])
                        balance = await get_star_balance(client, peer)
                        await asyncio.sleep(0.5)
                    except RuntimeError as e:
                        logging.error(f"Error: {e}")
                        continue
                    except Exception as e:
                        logging.error(f"Unexpected error: {e}")
                        continue

            await asyncio.sleep(0.5)

    except RuntimeError as e:
        logging.critical(f"Error connecting to Telegram: {e}")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Unexpected error in main: {e}")
        sys.exit(1)    
    finally:
        if client and client.is_connected():
            try:
                await client.disconnect()
            except Exception as e:
                logging.error(f"Error during disconnect: {e}")

if __name__ == "__main__":

    # Данные для Telegram API и создания клиента
    load_dotenv()
    API_HASH = os.getenv('API_HASH')
    API_ID = int(os.getenv('API_ID'))
    CHANNEL_NAME = os.getenv('CHANNEL_NAME')

    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except Exception as e:
        logging.critical(f"Error reading config.json: {e}")
        sys.exit(1)

    if not API_HASH or not API_ID or not CHANNEL_NAME:
        logging.critical("API_ID, API_HASH, or CHANNEL_NAME is not set in the .env file")
        sys.exit(1)

    try:
        asyncio.run(start_script(API_ID, API_HASH, CHANNEL_NAME, config))
    except KeyboardInterrupt:
        logging.info("Программа остановлена пользователем")
        sys.exit(0)

