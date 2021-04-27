from YSUNetAuthTools import YSUNetAuth
from logs import log
import sys
import parse

ysuAuth = YSUNetAuth()


def loginUser(users):
    for user in users:
        supports = user["support"].split(",")
        supports = [x for x in supports if int(x) in range(4)]

        for support in supports:
            re = ysuAuth.login(user["num"], user["password"], support)
            if re:
                break
            else:
                log.log(parse.netTypeToString(support) + "失败")


if __name__ == '__main__':
    log = log()
    print(ysuAuth.tst_net())
    ysuAuth.logout()
    ysuAuth.get_alldata()
    print(ysuAuth.tst_net())
    # # (False, '您本月可用流量已用尽，下月将自动恢复！')
    # print(loger.login("201811080333", "", "0"))
    # for i in range(100):
    #    print(loger.login("201811080333", "", "3"))

    # print([x for x in range(-1, 7) if x in range(4)])

    users = parse.getUsersFromFile("users.ini")

    loginUser(users)

    # loger.get_alldata();
    print(ysuAuth.tst_net())
    # loger.logout()
