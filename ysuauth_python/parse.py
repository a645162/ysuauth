import os

import platform

# from program_logs import log


def netTypeToString(type):
    if type == "0":
        return "校园网"
    elif type == "1":
        return "中国移动"
    elif type == "2":
        return "中国联通"
    elif type == "3":
        return "中国电信"


def getUsersFromFile(filename):
    users = []

    # 系统类型
    isWindows = False
    if str(platform.system()).find("Windows") != -1:
        isWindows = True

    encode1 = "utf-8"
    if isWindows:
        encode1 = "gbk"

    f = open(filename, 'r', encoding=encode1)
    try:
        f.read()
    except UnicodeDecodeError:
        encode1 = "utf-8"
    finally:
        f.close()

    with open(filename, 'r', encoding=encode1) as f:
        uList = f.readlines()
        for userOriginString in uList:
            userStringList = userOriginString.split("#")
            uSplitList = userStringList[0].strip().split("=")
            if len(uSplitList) != 2:
                continue
            pwd = ""
            num = uSplitList[0].strip()
            support = uSplitList[1].strip()
            if os.path.exists(num + ".pwd"):
                encode2 = "utf-8"
                if isWindows:
                    encode2 = "gbk"

                f = open(num + '.pwd', 'r', encoding=encode2)
                try:
                    p = f.read().strip()
                except UnicodeDecodeError:
                    encode2 = "utf-8"
                finally:
                    f.close()

                try:
                    with open(num + '.pwd', 'r', encoding=encode2) as f:
                        p = f.read().strip()
                except:
                    # TODO:LOG
                    pass
                    # log.log("读取文件错误")
                if len(p) != 0:
                    pwd = p
            if len(pwd) == 0:
                continue
            users.append({
                "num": num,
                "password": pwd,
                "support": support
            })
    return users
