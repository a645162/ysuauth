import os


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

    with open(filename, 'r') as f:
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
                try:
                    with open(num + '.pwd', 'r') as f:
                        p = f.read().strip()
                        if len(p) != 0:
                            pwd = p
                except:
                    log.log("读取文件错误")
            if len(pwd) == 0:
                continue
            users.append({
                "num": num,
                "password": pwd,
                "support": support
            })
    return users
