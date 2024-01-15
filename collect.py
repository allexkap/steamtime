import logging
import os
import re
import time
from json import load
from pathlib import Path

import requests


class TelegramStream:
    def __init__(self, token: str, chat_id: str) -> None:
        self.token = token
        self.chat_id = chat_id
        self.message = []

    def write(self, msg: str) -> None:
        self.message.append(msg)

    def flush(self) -> None:
        try:
            response = requests.post(
                url='https://api.telegram.org/bot{0}/sendMessage'.format(self.token),
                data={'chat_id': self.chat_id, 'text': ''.join(self.message)},
            )
            assert response.status_code
            self.message = []
        except:
            pass


telegram_handler = logging.StreamHandler(
    TelegramStream(
        os.environ['TELEGRAM_BOT_TOKEN'],
        os.environ['TELEGRAM_CHAT_ID'],
    )
)
telegram_handler.setLevel(logging.ERROR)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s %(filename)s:%(lineno)d %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=(
        logging.FileHandler(Path(__file__).with_suffix('.log'), 'a'),
        logging.StreamHandler(),
        telegram_handler,
    ),
)


def get_hours(profile_id: str) -> float:
    response = requests.get(f'https://steamcommunity.com/profiles/{profile_id}')
    assert response.status_code == 200

    res = re.search(r'([\d.]+) hours past 2 weeks', response.content.decode())
    hours = float(res[1]) if res else 0

    return hours


def main() -> None:
    with open('profiles.json') as file:
        profiles = load(file)

    for name in profiles:
        try:
            hours = get_hours(profiles[name])
            logging.info(f'{name=} {hours=}')
        except Exception as ex:
            logging.error(f'{name=}; {ex}')
        time.sleep(1)


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        logging.error(ex)
