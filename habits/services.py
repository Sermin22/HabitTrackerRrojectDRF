import requests
from config import settings


def send_telegram_massage(chat_id, message):
    '''Функция отправляет уведомление в Телеграм'''

    params = {
        "text": message,
        "chat_id": chat_id
    }
    requests.get(f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage', params=params)
