from datetime import datetime as dt
import sqlite3

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
d = cur.execute('select * from activity order by timestamp desc limit 9').fetchall()
r = '\n'.join(f'{dt.fromtimestamp(e[0]).ctime()}; {e[1]:>9}; {e[2]:5}' for e in d)
print(r)
