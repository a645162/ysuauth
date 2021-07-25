#!/usr/bin/env python3
# -*- coding:UTF-8 -*-
# 欢迎关注微信公众号：点滴技术
# 这里有靠谱、有价值、免费分享
import ntplib
import os, datetime
import ntp_hosts
import program_logs

hosts = ntp_hosts.getHosts()


def ntp_getTimeStamp():
    # 创建实例，NTPClient()是一个类
    t = ntplib.NTPClient()
    ok = False
    for host in hosts:
        try:
            # ntp server可以填写主机和域名，建议用域名
            # 缺省端口为ntp， 版本为2， 超时为5s
            # 作用：查询 NTP 服务器，并返回对象
            r = t.request(host, port='ntp', version=4, timeout=5)
            if r:
                # 显示的是时间戳
                t = r.tx_time
                ok = True
                program_logs.print1("从{}获取到时间{}".format(host,str(t)))
                # print("从{}获取到时间".format(host))
                break
        except Exception as e:
            program_logs.print1(repr(e))

    if ok:
        return t
    else:
        return None


def ntp_client():
    t = ntp_getTimeStamp()

    if t != None:
        # 使用datetime模块,格式化：x年x月x日 时:分:秒.毫秒
        # _date, _time = str(datetime.datetime.fromtimestamp(t))[:22].split(' ')
        _date, _time = datetime.datetime.fromtimestamp(t).strftime("%Y%m%d %H:%M:%S")[:22].split(' ')
        print("调整前时间是：", datetime.datetime.now())
        os.system("date")
        command = 'sudo date -s "{} {}"'.format(_date, _time)
        # os.system(command)
        print(command)
        print("调整后时间是：", datetime.datetime.now())
        os.system("date")


if __name__ == '__main__':
    # 适用于Windows
    ntp_client()
