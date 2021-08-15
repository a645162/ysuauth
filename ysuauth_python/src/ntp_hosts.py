import time

import program_logs

import os
import ntp_host
import ntp

import threading


class ntp_hosts():
    hosts_ = []

    maxLength = 0

    # ntp_host对象
    hosts = []

    def getMaxLength(self):
        for i in self.hosts:
            l = len(i.host_url)
            if l > self.maxLength:
                self.maxLength = l

    def getHosts(self):
        # 这里返回的是str list
        return ntp_host.get_list(self.hosts)

    def writeNewFile(self, path=""):
        if len(path) == 0:
            path = "ntp.list"

        with open(path, "w") as f:
            f.write("\n")

    def writeToFile(self, path=""):
        if len(path) == 0:
            path = "ntp.list"

        s = ""
        for i in self.hosts:
            s += i.host_url + "\n"
        with open(path, "w") as f:
            f.write(s)

    def getFromFiles(self, path=""):
        if len(path) == 0:
            path = "ntp_simple.list"

        if os.path.exists(path):
            h = []
            with open(path, "r") as f:
                s = f.read()
                for i1 in s.split("\n"):
                    i = i1.strip()
                    if len(i) != 0:
                        if i.find("#") != 0:
                            if i not in self.hosts_:
                                h.append(ntp_host.ntp_host(i))
                                self.hosts_.append(i)
            if len(h) != 0:
                self.hosts += h

    def initFile(self, path=""):
        if len(path) == 0:
            program_logs.print1("未指定NTP Hosts配置文件路径")
            path = "ntp.list"

        program_logs.print1(
            "开始读取NTP hosts文件 {}"
                .format(path)
        )

        if os.path.exists(path):
            program_logs.print1(
                "找到NTP Hosts配置文件：{}"
                    .format(path)
            )
            h = []
            with open(path, "r") as f:
                s = f.read()
                for i1 in s.split("\n"):
                    i = i1.strip()
                    if len(i) != 0:
                        if i.find("#") != 0:
                            if i not in self.hosts_:
                                h.append(ntp_host.ntp_host(i))
                                self.hosts_.append(i)
            if len(h) != 0:
                self.hosts = h
        else:
            program_logs.print1(
                "未找到NTP Hosts配置文件："
                "但已经创建 {}"
                    .format(path)
            )
            self.writeNewFile(path)

    def sort(self, restart_ping=False):
        hosts = self.hosts
        hosts_ = self.hosts_
        s = False
        if restart_ping:
            ntp_host.ping_all(hosts)
        max = len(hosts)
        for i in range(max):
            for j in range(i, max):
                if hosts[i] > hosts[j]:
                    hosts[i], hosts[j] = hosts[j], hosts[i]
                    hosts_[i], hosts_[j] = hosts_[j], hosts_[i]
                    s = True
        if s:
            self.hosts = hosts
            self.hosts_ = hosts_

    def output(self):
        for i in self.hosts:
            timeout = "Timeout:" + str(i.timeout) \
                      + " ({} ms)".format(str(i.ms))
            if i.timeout == 0:
                timeout = "Timeout: out of Time!"

            t = ""
            l = (self.maxLength - len(i.host_url))
            for j in range(l // 2 + 1):
                t += "  "
            for j in range(l % 2):
                t += " "

            program_logs.print1("NTP server:" + i.host_url + " "
                                + t + timeout)

    def delItem(self, num=0.0):
        i = 0
        l = len(self.hosts)
        while i < l:
            t = self.hosts[i].timeout
            if (num == 0 and t == 0) \
                    or (num == -1) \
                    or (num > 0 and (t == 0 or t * 1000 > num)):
                self.hosts.remove(self.hosts[i])
                self.hosts_.remove(self.hosts_[i])
                l -= 1
            else:
                i += 1

    def testAll(self):
        i = 0
        l = len(self.hosts)
        while i < l:
            if not self.hosts[i].testOK():
                self.hosts.remove(self.hosts[i])
                self.hosts_.remove(self.hosts_[i])
                l -= 1
            else:
                i += 1

    class ntpPingThread(threading.Thread):

        def __init__(self, num, queue, workingQueue):
            threading.Thread.__init__(self)
            self.num = num
            self.queue = queue
            self.workingQueue = workingQueue

        def run(self):
            while len(self.queue) != 0:
                thisMission = self.queue.pop()
                self.workingQueue.append(thisMission)
                thisMission.ping()
                self.workingQueue.remove(thisMission)

    class ntpTestThread(threading.Thread):

        def __init__(self, num, queue, workingQueue, okList):
            threading.Thread.__init__(self)
            self.num = num
            self.queue = queue
            self.workingQueue = workingQueue
            self.okList = okList

        def run(self):
            while len(self.queue) != 0:
                thisMission = self.queue.pop()
                self.workingQueue.append(thisMission)
                if thisMission.testOK():
                    self.okList.append(thisMission)
                self.workingQueue.remove(thisMission)

    queue = []
    ntpThreadPool_ping = []
    workingQueue = []

    queue_test = []
    ntpThreadPool_test = []
    workingQueue_test = []
    okList_test = []

    def pingAllMultThread(self, num=6):
        if num < 1:
            num = 1

        self.stopPing()
        self.queue = self.hosts.copy()

        for i in range(num):
            ntpPingThreadi = self.ntpPingThread(i,
                                                self.queue,
                                                self.workingQueue)

            self.ntpThreadPool_ping.append(ntpPingThreadi)
            ntpPingThreadi.start()

    def testAllMultThread(self, num=6):
        if num < 1:
            num = 1

        self.stopTest()
        self.queue_test = self.hosts.copy()

        for i in range(num):
            ntpPingThreadi = self.ntpTestThread(i,
                                                self.queue_test,
                                                self.workingQueue_test,
                                                self.okList_test
                                                )

            self.ntpThreadPool_test.append(ntpPingThreadi)
            ntpPingThreadi.start()

    def isPingAllMultThreadEnd(self):
        return len(self.queue) == 0 and len(self.workingQueue) == 0

    def isTestAllMultThreadEnd(self):
        return len(self.queue_test) == 0 and len(self.workingQueue_test) == 0

    def stopPing(self):
        if self.isPingAllMultThreadEnd():
            return True
        else:
            self.queue = []
            self.workingQueue = []
            self.ntpThreadPool_ping = []

    def updateListByTestResult(self):
        self.hosts = self.okList_test

    def stopTest(self):
        if self.isTestAllMultThreadEnd():
            return True
        else:
            self.queue_test = []
            self.workingQueue_test = []
            self.okList_test = []
            self.ntpThreadPool_test = []

    def isEmpty(self):
        return len(self.hosts)


if __name__ == "__main__":
    n = ntp_hosts()
    n.initFile()
    n.getFromFiles()
    n.getMaxLength()

    n.pingAllMultThread(6)
    while not n.isPingAllMultThreadEnd():
        time.sleep(1)
    print("结束Ping")
    n.output()
    n.delItem(100)
    n.testAllMultThread(6)
    while not n.isTestAllMultThreadEnd():
        time.sleep(1)
    n.updateListByTestResult()
    print("结束Test")
    # 想了想，没必要只保留10个，毕竟后面的基本上不会被访问到
    # while len(n.hosts) > 10:
    #     n.hosts.pop()

    n.sort()

    print()
    print()
    print()
    program_logs.print1("Sorted:")

    n.output()

    n.writeToFile()
