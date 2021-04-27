import time
from YSUNetAuthTools import YSUNetAuth
from logs import log
import parse

ysuAuth = YSUNetAuth()
users = parse.getUsersFromFile("users.ini")


def loginUser(users):
    for user in users:
        supports = user["support"].split(",")
        supports = [x for x in supports if int(x) in range(4)]

        for support in supports:
            re = ysuAuth.login(user["num"], user["password"], support)
            if re:
                log.log("连接"+ re)
                break
            else:
                log.log(parse.netTypeToString(support) + "失败")


while True:

    if not ysuAuth.tst_net():
        loginUser(users)

    time.sleep(10)
