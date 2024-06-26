import json
import re
import sys
from argparse import ArgumentParser
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep

import requests

from db import Activity


def assert_activity(activity: Activity, username: str, hours: float):
    if hours:
        return
    entry = activity.get_last(username)
    if entry is None:
        return
    ts = datetime.fromtimestamp(entry[0])
    delta = (datetime.now() - ts).seconds / 3600
    assert entry[2] <= delta, f'hours=0, record with {entry[2]}h at {ts}'


def every(step: timedelta, start: datetime | None = None):
    if start is None:
        start = datetime.now()
    while True:
        if start < datetime.now():
            start += step
            yield
        sleep(1)


def printerr(*args, **kwargs):
    return print(*args, **kwargs, file=sys.stderr)


def get_hours(profile_id: str) -> float:
    response = requests.get(f'https://steamcommunity.com/profiles/{profile_id}')
    assert response.status_code == 200, f'steam {response.status_code=} != 200'
    res = re.search(r'([\d.]+) hours past 2 weeks', response.content.decode())
    hours = float(res[1]) if res else 0
    return hours


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-p',
        '--period',
        help='period in minutes',
        default=30,
        type=int,
    )
    parser.add_argument(
        '-d',
        '--db_path',
        help='path to sqlite3 database',
        default='./db.sqlite3',
        type=Path,
    )
    parser.add_argument(
        '-u',
        '--profiles_path',
        help='path to json file with list of profiles',
        default='./profiles.json',
        type=Path,
    )
    args = parser.parse_args()
    args.period = timedelta(minutes=args.period)
    return args


if __name__ == '__main__':
    args = parse_args()

    activity = Activity(args.db_path)
    with open(args.profiles_path) as file:
        profiles = json.load(file)

    start = datetime.now().replace(minute=0, second=0, microsecond=0)
    start += ((datetime.now() - start) // args.period + 1) * args.period
    for _ in every(step=args.period, start=start):
        pending_profiles = set(profiles)
        for attempt in range(3):
            for username in sorted(pending_profiles):
                try:
                    hours = get_hours(profiles[username])
                    assert_activity(activity, username, hours)
                    activity.insert(username, hours)
                    pending_profiles.remove(username)
                except Exception as ex:
                    printerr(f'{datetime.now().ctime()}; {username}; {repr(ex)}')
                sleep(2)
            if not pending_profiles:
                break
            sleep(60)
        for username in pending_profiles:
            activity.insert(username, None)
