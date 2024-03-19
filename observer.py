import sqlite3
from pathlib import Path
from datetime import datetime


db_path = Path('db.sqlite3')


db_create_table = '''
create table if not exists activity (
    timestamp integer,
    account text,
    hours real
) strict
'''
db_insert_row = 'insert into activity values (?, ?, ?)'

con = sqlite3.connect(db_path)
cur = con.cursor()

cur.execute(db_create_table)
con.commit()


def add_entry(user, value):
    ts = int(datetime.utcnow().timestamp())
    cur.execute(db_insert_row, (ts, user, value))
    con.commit()


con.close()
