import datetime


def isInTime(t1=(6, 0), t2=(11, 30)):
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    return (hour > t1[0] or (hour == t1[0] and minute >= t1[1])) \
           and \
           (hour < t2[0] or (hour == t2[0] and minute <= t2[1]))
