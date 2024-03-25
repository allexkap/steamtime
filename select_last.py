from datetime import datetime as dt
from pathlib import Path

from db import Activity

activity = Activity(Path('db.sqlite3'))
d = activity.tail(9)
r = '\n'.join(f'{dt.fromtimestamp(e[0]).ctime()}; {e[1]:>9}; {e[2]:5}' for e in d)
print(r)
