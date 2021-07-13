import apptime
from YSUNetAuthTools import YSUNetAuth
from program_logs import log
import parse

import datetime
import time
import threading

from dingtalk import DingTalk
import datetime

dt = DingTalk()

dt.getFromFiles()

delayTime = 10


class myThread(threading.Thread):
    def __init__(self, time, type=False):
        threading.Thread.__init__(self)
        self.time = time
        self.type = type

    def run(self):
        nowtime = datetime.datetime.now()
        print("\t\t\t开始线程({})："
              .format(datetime.datetime.strftime(nowtime, '%Y年%m月%d日 %H:%M:%S'))
              + self.name)
        if not type:
            program = {
                "msgtype": "link",
                "link": {"text": "[{}] 联网成功！".format(self.time),
                         "title": "联网成功",
                         "picUrl": "https://ysu.edu.cn/images/favicon.png",
                         "messageUrl": "http://auth.ysu.edu.cn"
                         },
                "at": {
                    "isAtAll": True
                }
            }
        else:
            program = {
                "msgtype": "markdown",
                "markdown": {
                    "title": "断网时间",
                    "text": "#### 断网时间 @全体成员 \n > 断网时间为{}\n"
                            " > ![icon](https://ysu.edu.cn/images/favicon.png)\n > ###### {} 发送\n"
                            "[11A633网络](http://www.dingtalk.com) \n".format(self.time, nowtime)
                },
                "at": {
                    "isAtAll": True
                }
            }
        print("\t\t\t延时{}秒后发送{}连接成功的消息！".format(str(delayTime), self.time))
        time.sleep(delayTime)
        print("\t\t\t延时完毕开始发送{}连接成功的消息！".format(self.time))
        ok = False
        while not ok:
            try:
                f = dt.sendMsg(program)
            except:
                print("发送出错，等待1s后再次发送。")
                time.sleep(1)
                pass
            else:
                ok = True

        nowtime = datetime.datetime.now()
        print("\t\t\t退出线程({})："
              .format(datetime.datetime.strftime(nowtime, '%Y年%m月%d日 %H:%M:%S'))
              + self.name)


ysuAuth = YSUNetAuth()
users = parse.getUsersFromFile("users.ini")
print(users)


def loginUser(users):
    for user in users:
        supports = user["support"].split(",")
        supports = [x for x in supports if int(x) in range(4)]

        for support in supports:
            re = ysuAuth.login(user["num"], user["password"], support)
            if re[0]:
                print("[", datetime.datetime.now(), "]", "连接", re)
                break
            else:
                print("[", datetime.datetime.now(), "]",
                      parse.netTypeToString(support) + "失败(", re[1], ")")


last = -1
disConnectedTime = ""
while True:

    now = datetime.datetime.now()
    hour = now.hour

    if apptime.isInTime((6, 1), (23, 25)):
        if not ysuAuth.tst_net():
            print("[", now, "]", "Not Connect!!!!!")
            if last == 2:
                disConnectedTime = False
            last = 1
            loginUser(users)
        else:
            print("[", now, "]", "connected!")
            if last != 2:
                myThread(datetime.datetime.strftime(now, '%Y年%m月%d日 %H:%M:%S'), False).start()
            last = 2
            if len(disConnectedTime) != 0:
                myThread(disConnectedTime, True).start()
    else:
        print("[", now, "]", "不在工作时间！")
        last = 0
        time.sleep(60)

    print("-----------------------------------------------------")
    print()
    time.sleep(10)

# def execfile(filepath, globals=None, locals=None):
#     if globals is None:
#         globals = {}
#     globals.update({
#         "__file__": filepath,
#         "__name__": "__main__",
#     })
#     with open(filepath, 'rb') as file:
#         exec(compile(file.read(), filepath, 'exec'), globals, locals)


# if __name__ == '__main__':
#     # pass
#     # runfile()
#     execfile("./main.py")
