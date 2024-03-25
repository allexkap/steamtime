from argparse import ArgumentParser
from datetime import datetime as dt
from pathlib import Path

from db import Activity

parser = ArgumentParser()
parser.add_argument('-d', default='./db.sqlite3', type=Path)
parser.add_argument('-n', default=9, type=int)
args = parser.parse_args()

activity = Activity(args.d)
t = activity.tail(args.n)
r = '\n'.join(f'{dt.fromtimestamp(e[0]).ctime()}; {e[1]:>9}; {str(e[2]):>5}' for e in t)
print(r)
