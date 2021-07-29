import program_logs

import os
import ntp_host


class ntp_hosts():
    hosts_1 = [
        # 'ntp.tuna.tsinghua.edu.cn',
        'time.ustc.edu.cn',
        'ntp.ntsc.ac.cn',
        'ntp.aliyun.com',
        'ntp.neu.edu.cn',
        'ntp.nju.edu.cn',
        'time.buptnet.edu.cn',
        's1d.time.edu.cn',
        'time.asia.apple.com',
    ]
    hosts_2 = ['0.cn.pool.ntp.org', '1.cn.pool.ntp.org', '2.cn.pool.ntp.org', '3.cn.pool.ntp.org']
    hosts_ = []
    hosts_ += hosts_1
    hosts_ += hosts_2

    # ntp_host对象
    hosts = []

    def getHosts(self):
        # 这里返回的是str list
        return ntp_host.get_list(self.hosts)

    def initFile(self, path=""):
        if len(path) == 0:
            path = "ntp.list"

        if not os.path.exists(path):
            s = ""
            for i in self.hosts:
                s += i + "\n"
            with open(path, "w")as f:
                f.write(s)
            self.hosts = ntp_host.init_by_list(self.hosts_)
        else:
            h = []
            with open(path, "r")as f:
                s = f.read()
                for i1 in s.split("\n"):
                    i = i1.strip()
                    if len(i) != 0:
                        h.append(ntp_host.ntp_host(i))
            self.hosts = h

    def sort(self, restart_ping=False):
        hosts = self.hosts
        if restart_ping:
            ntp_host.ping_all(hosts)
        max = len(hosts)
        for i in range(max):
            for j in range(i, max):
                if hosts[i] > hosts[j]:
                    hosts[i], hosts[j] = hosts[j], hosts[i]
        pass

    def output(self):
        for i in self.hosts:
            program_logs.print1(i.host_url + " " + str(i.timeout))


if __name__ == "__main__":
    n = ntp_hosts()
    n.initFile()
    n.sort()
    n.output()
