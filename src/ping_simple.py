from ping3 import ping

import program_logs


def ping_host(ip, ping_tag=-1):
    """
    获取节点的延迟的作用
    :param ip:
    :param ping_tag: log输出时的tag
    :return delay time:
    """
    ip_address = ip
    response = ping(ip_address)
    # log太多了，烦死了
    program_logs.print1("ping " + ip + " original " + str(response) + " 延迟", tag=ping_tag)
    if response is not None:
        delay = int(response * 1000)
        program_logs.print1("ping " + ip + " " + str(delay) + "ms 延迟")
        return response
    else:
        return 0


if __name__ == "__main__":
    ping_host('www.baidu.com')
