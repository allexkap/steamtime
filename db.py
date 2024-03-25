import sqlite3
from datetime import datetime


class Activity:

    _create_table_cmd = '''
        create table if not exists activity (
            timestamp integer not null,
            account text not null,
            hours real
        )
    '''
    _insert_row_cmd = 'insert into activity values (?, ?, ?)'
    _select_tail_cmd = 'select * from activity order by timestamp desc limit ?'
    _select_last_by_user_cmd = '''
        select * from activity
        where account = ? and hours is not null
        order by timestamp desc limit 1
    '''

    def __init__(self, path: str):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.cur.execute(self._create_table_cmd)
        self.con.commit()

    def insert(self, user: str, value: float | None):
        ts = int(datetime.now().timestamp())
        self.cur.execute(self._insert_row_cmd, (ts, user, value))
        self.con.commit()

    def get_last(self, user: str):
        res = self.cur.execute(self._select_last_by_user_cmd, (user,))
        return res.fetchone()

    def tail(self, n: int = 5):
        res = self.cur.execute(self._select_tail_cmd, (n,))
        return res.fetchall()

    def __del__(self):
        self.con.close()
