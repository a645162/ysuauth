import apptime
from YSUNetAuthTools import YSUNetAuth
# from program_logs import log
import parse

import datetime
import time
import threading

from dingtalk import DingTalk
import datetime

import program_logs

import parseDingTalkJson

program_logs.print1('程序开始运行')

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
        program_logs.print1("\t\t\t启动钉钉发信线程({})："
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
        program_logs.print1("\t\t\t延时{}秒后发送{}连接成功的消息！".format(str(delayTime), self.time))
        time.sleep(delayTime)
        program_logs.print1("\t\t\t延时完毕开始发送{}连接成功的消息！".format(self.time))
        ok = False
        while not ok:
            try:
                f = dt.sendMsg(program)
                program_logs.print1("DingTalk Response:" + f.text)
            except:
                program_logs.print1("发送出错，等待10s后再次发送。", True)
                time.sleep(10)
                pass
            else:
                if f != None and len(f.text) != 0:
                    jsonStr = str(f.text)
                    ok = parseDingTalkJson.isDingTalkOk(jsonStr)
                else:
                    program_logs.print1("取不到返回吗？！", True)
                    ok = True

        nowtime = datetime.datetime.now()
        program_logs.print1("\t\t\t退出钉钉发信线程({})："
                            .format(datetime.datetime.strftime(nowtime, '%Y年%m月%d日 %H:%M:%S'))
                            + self.name)


ysuAuth = YSUNetAuth()
users = parse.getUsersFromFile("users.ini")
program_logs.print1(users)


def loginUser(users):
    for user in users:
        supports = user["support"].split(",")
        supports = [x for x in supports if int(x) in range(4)]

        for support in supports:
            re = ysuAuth.login(user["num"], user["password"], support)
            if re[0]:
                program_logs.print1("连接" + re)
                break
            else:
                program_logs.print1(parse.netTypeToString(support) + "失败(" + re[1] + ")"
                                    , True)


last = -1
disConnectedTime = ""
while True:

    now = datetime.datetime.now()
    hour = now.hour

    if apptime.isInTime((6, 1), (23, 25)):
        if not ysuAuth.tst_net():
            program_logs.print1("Not Connect!!!!!")
            if last == 2:
                disConnectedTime = False
            last = 1
            loginUser(users)
        else:
            program_logs.print1("connected!")
            if last != 2:
                myThread(datetime.datetime.strftime(now, '%Y年%m月%d日 %H:%M:%S'), False).start()
            last = 2
            if len(disConnectedTime) != 0:
                myThread(disConnectedTime, True).start()
    else:
        program_logs.print1("不在工作时间！")
        last = 0
        time.sleep(60)

    # program_logs.print1("-----------------------------------------------------")
    # print()
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
