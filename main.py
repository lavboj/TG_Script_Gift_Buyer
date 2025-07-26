# Стандартные библиотеки
import logging
import asyncio
import os
import sys

# Сторонние библиотеки
from dotenv import load_dotenv

# Локальные модули/пакеты
from service.balance import get_star_balance
from service.buy import buy_gift
from service import gift_fetcher, auth
from utils import log_config

log_config.setup_logging(level=logging.DEBUG) 

async def start_script(api_id, api_hash):
    
    try:
        #Создание клиента и подключение к Telegram
        auth_client = auth.ClientAuthenticator('authClient', api_id, api_hash)
        client = await auth_client.connect()

        #Создание peer канала и peer пользователя
        channel_peer = await client.get_input_entity(CHANNEL_NAME)
        peer = await auth_client.get_input_peer()
    except RuntimeError as e:
        logging.critical(f"Error connecting to Telegram: {e}")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Unexpected error in main: {e}")
        sys.exit(1)
    
    print("Сканируем подарки...")

    #Основной цикл который вводит скрипт в сканирование подарков и их покупку
    while True:
        # Получение списка подарков по заданным параметрам
        if not client.is_connected():
            logging.critical("Reconnection failed")
            sys.exit(1)
        try:
            gift_list = await gift_fetcher.gift_filter(client, 200, 2000, 250000)
            balance = await get_star_balance(client, peer)
        except RuntimeError as e:
            logging.error(f"Error: {e}")
            continue
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            continue

        # Если есть подарки, начинаем их покупку опираясь на текущий баланс
        if balance < 200:
            print("Деньги кончились, отключаемся...")
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
        
    await client.disconnect()
    sys.exit(0)

if __name__ == "__main__":

    # Данные для Telegram API и создания клиента
    load_dotenv()
    API_HASH = os.getenv('API_HASH')
    API_ID = int(os.getenv('API_ID'))
    CHANNEL_NAME = os.getenv('CHANNEL_NAME')

    if not API_HASH or not API_ID or not CHANNEL_NAME:
        logging.critical("API_ID, API_HASH, or CHANNEL_NAME is not set in the .env file")
        sys.exit(1)

    asyncio.run(start_script(API_ID, API_HASH))

