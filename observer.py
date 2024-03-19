import sqlite3
from pathlib import Path
from datetime import datetime


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

    def insert(self, user: str, value: float):
        ts = int(datetime.utcnow().timestamp())
        self.cur.execute(self._insert_row_cmd, (ts, user, value))
        self.con.commit()

    def tail(self, n: int = 5):
        res = self.cur.execute(self._select_tail_cmd, (n,))
        return res.fetchall()

    def __del__(self):
        self.con.close()
