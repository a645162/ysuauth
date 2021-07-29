# -*- coding: utf-8 -*-
import random
import os
import time
import threading
import datetime

import apptime
# from YSUNetAuthTools import YSUNetAuth
import YSUNetAuthTools
import parse

from dingtalk import DingTalk

import program_logs

import parseDingTalkJson
import config

import time_p
import ntp
import ntp_hosts

restartFilename = "restart.ysuauth"
if config.isFileExist(restartFilename):
    program_logs.print1('\t\t\t\t\t程序重启。')
    os.remove(restartFilename)

program_logs.print1('程序开始运行')

dt = DingTalk()

dt.getFromFiles()

delayTime = 10

my_ntp_hosts_class = ntp_hosts.ntp_hosts()
my_ntp_hosts_class.initFile()
my_ntp_hosts = my_ntp_hosts_class.getHosts()


# print("hosts")
# print(hosts)


class dingTalkThread(threading.Thread):
    def __init__(self, time, type=False, ntp_hosts=None):
        threading.Thread.__init__(self)
        self.time = time
        self.type = type
        self.ntp_hosts = ntp_hosts

    def run(self):
        nowtime = datetime.datetime.now()
        program_logs.print1("\t\t\t启动钉钉发信线程({})："
                            .format(datetime.datetime.strftime(nowtime, '%Y年%m月%d日 %H:%M:%S'))
                            + self.name)
        typeStr = "连接成功"

        if not self.type:
            msg_dict = {
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
            typeStr = "错误"
            msg_dict = {
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
        program_logs.print1(
            "\t\t\t延时{}秒后发送{}{}的消息！"
                .format(str(delayTime), self.time, typeStr)
        )
        time.sleep(delayTime)
        program_logs.print1(
            "\t\t\t延时完毕开始发送{}{}的消息！"
                .format(self.time, typeStr)
        )
        ok = False
        while not ok:
            try:
                if self.ntp_hosts is not None and len(self.ntp_hosts) != 0:
                    t = ntp.ntp_getTimeStamp(self.ntp_hosts)
                    program_logs.print1("NTP TIMESTAMP:{}".format(str(t)))
                else:
                    t = 0
                dt.getUrl(timestamp=t)
                f = dt.sendMsg(msg_dict)
                program_logs.print1("DingTalk Response:" + f.text)
            except Exception as e:
                # print(msg_dict)
                program_logs.print1(repr(e))
                program_logs.print1("发送出错，等待20s后再次发送。", True)
                time.sleep(20)
                raise e
            else:
                if f != None and len(f.text) != 0:
                    jsonStr = str(f.text)
                    ok = parseDingTalkJson.isDingTalkOk(jsonStr)
                    if not ok:
                        if ok.testDingTalkError(jsonStr, "too fast"):
                            time.sleep(60 + random.randint(10, 30))
                        elif ok.testDingTalkError(jsonStr, "invalid timestamp"):
                            dt.getUrl()

                else:
                    program_logs.print1("取不到返回吗？！", True)
                    ok = True

        nowtime = datetime.datetime.now()
        program_logs.print1("\t\t\t退出钉钉发信线程({})："
                            .format(datetime.datetime.strftime(nowtime, '%Y年%m月%d日 %H:%M:%S'))
                            + self.name)


# YSUNetAuthTools.YSUNetAuth
ysuAuth = YSUNetAuthTools.YSUNetAuth()
users = parse.getUsersFromFile("users.ini")
program_logs.print1(users)


def loginUser(users):
    for user in users:
        supports = user["support"].split(",")
        supports = [x for x in supports if int(x) in range(4)]

        for support in supports:
            re = ysuAuth.login(user["num"], user["password"], support)
            if re[0]:
                program_logs.print1("连接" + str(re))
                break
            else:
                program_logs.print1(parse.netTypeToString(support) + "失败(" + re[1] + ")"
                                    , True)


last = -1
disConnectedTime = ""
threadPool = []
if __name__ == "__main__":
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
                if last != 2:
                    program_logs.print1("Turn to connected!")
                    program_logs \
                        .asynchronismPrintThread(
                        "Turn to connected!",
                        my_ntp_hosts
                    )

                    ntp_timestamp = ntp.ntp_getTimeStamp(my_ntp_hosts)
                    if ntp_timestamp == 0:
                        ntp_time_str = "???有毒吧？？？\n凭什么获取不到？？？"
                        program_logs.print1("NTP时间获取出错！！！")
                        program_logs.print1(ntp_time_str)
                        program_logs.print1("my_ntp_hosts")
                        program_logs.print1(my_ntp_hosts)

                    else:
                        ntp_time_str = \
                            datetime.datetime.fromtimestamp(ntp_timestamp)\
                                .strftime("%Y年%m月%d日 %H:%M:%S")

                    thread = \
                        dingTalkThread(
                            datetime.datetime.strftime(now, '%Y年%m月%d日 %H:%M:%S')
                            + "\n NTP时间为：" + ntp_time_str
                            ,
                            False,
                            my_ntp_hosts
                            # None
                        )
                    thread.start()
                    threadPool.append(thread)
                last = 2
                if len(disConnectedTime) != 0:
                    threadPool.append(
                        dingTalkThread(disConnectedTime, True)
                    )
                    threadPool[len(threadPool)].start()
        else:
            program_logs.print1("不在工作时间！")
            last = 0
            time.sleep(60)

        if config.isFileExist("restart.ysuauth"):
            program_logs.print1("检测到重启程序指令。")
            program_logs.print1("跳出检测循环。")
            program_logs.print1("-----------------------------------------------------")
            break

        time.sleep(10)
