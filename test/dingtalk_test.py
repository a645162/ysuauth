import datetime
import threading
import time

import ntp
import program_logs
from dingtalk import DingTalk

dt = DingTalk()

dt.getFromFiles()


class myThread(threading.Thread):
    def __init__(self, time):
        threading.Thread.__init__(self)
        self.time = time

    def run(self):
        nowtime = datetime.datetime.now()
        print("开始线程({})："
              .format(datetime.datetime.strftime(nowtime, '%Y年%m月%d日 %H:%M:%S'))
              + self.name)
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

        ok = False
        while not ok:
            try:
                t = ntp.ntp_getTimeStamp()
                program_logs.print1("NTP TIMESTAMP:{}".format(str(t)))
                dt.getUrl(timestamp=t)
                f = dt.sendMsg(program)
            except:
                print("发送出错，等待1s后再次发送。")
                time.sleep(1)
                pass
            else:
                ok = True

        # dt.sendMsg(program)
        nowtime = datetime.datetime.now()
        print("退出线程({})："
              .format(datetime.datetime.strftime(nowtime, '%Y年%m月%d日 %H:%M:%S'))
              + self.name)


if __name__ == '__main__':
    nowtime = datetime.datetime.now()
    thread1 = myThread(datetime.datetime.strftime(nowtime, '%Y年%m月%d日 %H:%M:%S'))
    thread1.start()
