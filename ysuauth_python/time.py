import datetime

now = datetime.datetime.now()
hour = now.hour

if hour >= 6 and (hour < 23 or (hour == 23 and now.minute <= 25)):
    print("ok")
else:
    print("不再工作时间！")
