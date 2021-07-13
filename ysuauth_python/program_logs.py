import datetime
import logging

import apptime

logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                    filename='{}.log'.format(datetime.datetime.strftime(apptime.getNow(), '%Y年%m月%d日 %H:%M:%S')),
                    filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                    # a是追加模式，默认如果不写的话，就是追加模式
                    format=
                    '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    # 日志格式
                    )


#
# class log():
#     def log(self, log):
#         print("[", datetime.datetime.now(), "]", log)

def print1(text, error=False):
    typeStr = "Info"
    if error:
        logging.error(text)
        typeStr = "Error!!!"
    else:
        logging.info(text)
    print("[", datetime.datetime.now(), "]({})".format(typeStr), text)
