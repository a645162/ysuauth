hosts1 = [
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
hosts2 = ['0.cn.pool.ntp.org', '1.cn.pool.ntp.org', '2.cn.pool.ntp.org', '3.cn.pool.ntp.org']
hosts = []
hosts += hosts1
hosts += hosts2

def getHosts():
    return hosts

