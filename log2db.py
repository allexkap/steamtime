import re
from datetime import datetime

from db import Activity


def insert(activity, user, value, now):
    ts = int(now.timestamp())
    activity.cur.execute(activity._insert_row_cmd, (ts, user, value))
    activity.con.commit()


if __name__ == '__main__':
    activity = Activity('./log.sqlite3')
    with open('./collect.log') as file:
        for line in file:
            r = re.match(r'\[(.*?)\].*?name=\'(.*?)\'.*?hours=(.*)$', line)
            if r is None:
                continue
            now = datetime.fromisoformat(r[1])
            user = r[2]
            hours = float(r[3])

            if hours == 0:
                entry = activity.get_last(user)
                if entry is not None:
                    ts = datetime.fromtimestamp(entry[0])
                    delta = (now - ts).seconds / 3600
                    if entry[2] > delta:
                        hours = None

            insert(activity, user, hours, now)
