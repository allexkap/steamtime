import sqlite3
from argparse import ArgumentParser
from datetime import datetime, timedelta
from pathlib import Path
from time import sleep


class Activity:

    _create_table_cmd = '''
        create table if not exists activity (
            timestamp integer not null,
            account text not null,
            hours real
        ) strict
    '''
    _insert_row_cmd = 'insert into activity values (?, ?, ?)'
    _select_tail_cmd = 'select * from activity order by timestamp desc limit ?'

    def __init__(self, path: Path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.cur.execute(self._create_table_cmd)
        self.con.commit()

    def insert(self, user: str, value: float):
        ts = int(datetime.utcnow().timestamp())
        self.cur.execute(self._insert_row_cmd, (ts, user, value))
        self.con.commit()

    def tail(self, n: int = 5):
        res = self.cur.execute(self._select_tail_cmd, (n,))
        return res.fetchall()

    def __del__(self):
        self.con.close()


def every(step: timedelta, start: datetime | None = None):
    if start is None:
        start = datetime.now()
    while True:
        if start < datetime.now():
            start += step
            yield
        sleep(1)


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
        help='path to sqlite3 database',
        default='./profiles.json',
        type=Path,
    )
    args = parser.parse_args()
    args.period = timedelta(minutes=args.period)
    return args


if __name__ == '__main__':
    args = parse_args()

    start = datetime.now().replace(minute=0, second=0, microsecond=0)
    start += ((datetime.now() - start) // args.period + 1) * args.period
    for _ in every(step=args.period, start=start):
        pass
