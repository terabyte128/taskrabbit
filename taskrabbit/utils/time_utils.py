from datetime import datetime
from string import Formatter


def get_total_time(raw_time_logs):
    # There's probably a better way to do this but I don't really care
    hacky_time = datetime(1970, 1, 1)
    grand_total_time = datetime(1970, 1, 1)

    # Calculate totals
    for aTime in raw_time_logs:
        if aTime.exit_time:
            aTotal = aTime.exit_time - aTime.entry_time
            grand_total_time += aTotal

    return grand_total_time - hacky_time


def strfdelta(tdelta, fmt):
    f = Formatter()
    d = {}
    l = {'D': 86400, 'H': 3600, 'M': 60, 'S': 1}
    k = map(lambda x: x[1], list(f.parse(fmt)))
    rem = int(tdelta.total_seconds())

    for i in ('D', 'H', 'M', 'S'):
        if i in k and i in l.keys():
            d[i], rem = divmod(rem, l[i])

    return f.format(fmt, **d)
