import os
import getenv
import platform
import config
import program_logs


# from program_logs import logs


def netTypeToString(type):
    if type == "0":
        return "校园网"
    elif type == "1":
        return "中国移动"
    elif type == "2":
        return "中国联通"
    elif type == "3":
        return "中国电信"


def getUsersFromEnv():
    users = []
    u = getenv.get_user()

    if u is None or len(u) == 0:
        return None
    u = u.strip()

    if len(u) == 0:
        return None

    uList = u.split("&")

    for userOriginString in uList:
        userStringList = userOriginString.split("#")
        uSplitList = userStringList[0].strip().split("=")
        if len(uSplitList) != 2:
            continue
        num = uSplitList[0].strip()
        support = uSplitList[1].strip()
        pwd = getenv.getPwd(num)
        if pwd is None or len(pwd) == 0 or len(num) == 0 or len(support) == 0:
            continue

        users.append({
            "num": num,
            "password": pwd,
            "support": support
        })

    return users


def getUsersFromFile(filename):
    if not os.path.exists(filename):
        return None
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

    dir_and_filename = config.getDirAndFileName(filename.strip())

    with open(filename, 'r', encoding=encode1) as f:
        uList = f.readlines()
        # print(uList)
        for userOriginString in uList:
            userStringList = userOriginString.split("#")
            vaildStr = userStringList[0].strip()
            if len(vaildStr) == 0:
                continue
            # print(vaildStr)
            uSplitList = vaildStr.split("=")
            if len(uSplitList) != 2:
                continue
            pwd = ""
            num = uSplitList[0].strip()
            support = uSplitList[1].strip()

            # 适配绝对路径
            pwd_path = dir_and_filename[0]
            if len(pwd_path) != 0:
                pwd_path += "/"
            pwd_path += num + '.pwd'

            if os.path.exists(pwd_path):
                encode2 = "utf-8"
                if isWindows:
                    encode2 = "gbk"

                program_logs.print1("正在检测用户{}的密码文件{}".format(num, pwd_path))

                f = open(pwd_path, 'r', encoding=encode2)
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
                    # logs.logs("读取文件错误")
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
