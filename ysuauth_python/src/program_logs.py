import datetime
import logging

import apptime
import ntp

import threading

import ntp_hosts

import getenv

log_path = getenv.getLogsPath()
if len(log_path) != 0:
    log_path += "/"



logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename='{}.log'.format(
                        log_path + datetime.datetime.strftime(apptime.getNow(), 'ysuauth_%Y%m%d_%H%M%S')),
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )


def print1(text="", error=False, timestamp=0):
    if isinstance(text, list):
        l = text
        text = ""
        for i in l:
            text += str(i) + "\n"
        text = text.strip()
    if timestamp == 0:
        timestamp = datetime.datetime.now()
    else:
        timestamp = ntp.getDatetime(timestamp)
    type_str = "Info"
    if error:
        logging.error(text)
        type_str = "!!!Error!!!"
    else:
        logging.info(text)
    s = "[" + str(timestamp) + "]({})".format(type_str) + "  " + text
    print(s)


msgQueue = []


def asynchronous_print(text="", error=False, ntp_hosts=None):
    asyn = asynchronousPrintThread(msgQueue, text, error, ntp_hosts)
    msgQueue.append((text, error))
    asyn.start()


class asynchronousPrintThread(threading.Thread):
    def __init__(self, queue, text="", error=False, ntp_hosts=None):
        threading.Thread.__init__(self)
        self.queue = queue
        self.text = text
        self.error = error
        self.ntp_hosts = ntp_hosts

    def run(self):
        msg = self.queue.pop()
        if self.ntp_hosts is not None:
            t = ntp.ntp_getTimeStamp(ntp_hosts)
        else:
            t = 0

        print1("( Asynchronous Print ) " + msg[0], msg[1], t)


def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)
