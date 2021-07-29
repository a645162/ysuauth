import ping_simple


def ping_all(hosts_list):
    for i in hosts_list:
        i.ping()


def init_by_list(hosts_list):
    re = []
    for i in hosts_list:
        url = str(i).strip()
        if len(url) != 0:
            re.append(ntp_host(url))
    return re


def get_list(hosts_list):
    re = []
    for i in hosts_list:
        re.append(i.host_url)
    return re


class ntp_host():
    host_url = ""
    timeout = 0

    def __init__(self, host_url):
        self.host_url = host_url
        self.timeout = 0

    def ping(self):
        if len(self.host_url) == 0:
            return 0
        timeout = ping_simple.ping_host(self.host_url)
        self.timeout = timeout
        return timeout

    def __get__(self, other):
        if self.timeout == 0:
            self.ping()
        if other.timeout == 0:
            other.ping()
        return self.timeout > other.timeout

    def __lt__(self, other):
        if self.timeout == 0:
            self.ping()
        if other.timeout == 0:
            other.ping()
        return self.timeout < other.timeout

    def __ge__(self, other):
        if self.timeout == 0:
            self.ping()
        if other.timeout == 0:
            other.ping()
        return self.timeout >= other.timeout

    def __le__(self, other):
        if self.timeout == 0:
            self.ping()
        if other.timeout == 0:
            other.ping()
        return self.timeout <= other.timeout

# >    __get__
# <    __lt__
# >=    __ge__
# <=    __le__
