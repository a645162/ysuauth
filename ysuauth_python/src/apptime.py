import datetime

from dateutil.parser import parse


def getNow():
    return datetime.datetime.now()


def isInTime(t1=(6, 0), t2=(11, 30)):
    now = getNow()
    hour = now.hour
    minute = now.minute
    return (hour > t1[0] or (hour == t1[0] and minute >= t1[1])) \
           and \
           (hour < t2[0] or (hour == t2[0] and minute <= t2[1]))


def parse_str2datetime(str):
    return parse(str)


def dateDiffInHours(t1, t2):
    td = t2 - t1
    return td.days * 24 + td.seconds / 3600 + 1


def dateDiff(a, b):
    if type(a) != datetime.datetime or type(b) != datetime.datetime:
        return None

    if a.timestamp() < b.timestamp():
        a, b = b, a

    d = a - b

    hour = int(d.seconds // 3600)
    r = d.seconds % 3600
    minutes = int(r // 60)
    seconds = int(r % 60)

    return d.days, hour, minutes, seconds


if __name__ == "__main__":
    t1 = datetime.datetime(2016, 3, 31, 0)
    t2 = datetime.datetime(2016, 6, 8, 2)

    a = datetime.datetime(2016, 6, 6, 13, 0, 1)
    b = datetime.datetime(2016, 6, 8, 12, 2, 32)
    # print(dateDiffInHours(t1, t2))

    # if a.timestamp() < b.timestamp():
    #     a, b = b, a
    # print((a - b).days)
    # print((a - b).seconds)
    #
    # hour = int((a - b).seconds // 3600)
    # r = (a - b).seconds % 3600
    # minutes = int(r // 60)
    # seconds = int(r % 60)

    # print((a - b).seconds / 3600)

    # print(hour, minutes, seconds)

    r = dateDiff(a, b)
    print(r[0], r[1], r[2], r[3])
