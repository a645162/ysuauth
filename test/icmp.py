# encoding:utf-8
import time
import struct
import socket
import select


# 检验和
def chesksum(data):
    n = len(data)
    m = n % 2
    sum = 0
    for i in range(0, n - m, 2):
        # 传入data以每两个字节（十六进制）通过ord转十进制，第一字节在低位，第二个字节在高位
        sum += (data[i]) + ((data[i + 1]) << 8)
        sum = (sum >> 16) + (sum & 0xffff)
    if m:
        sum += (data[-1])
        sum = (sum >> 16) + (sum & 0xffff)

    # 取反
    answer = ~sum & 0xffff
    #  主机字节序转网络字节序列
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def request_ping(data_type, data_code, data_checksum, data_ID, data_Sequence, payload_body):
    #  把字节打包成二进制数据
    imcp_packet = struct.pack('>BBHHH32s', data_type, data_code, data_checksum, data_ID, data_Sequence, payload_body)
    # 获取校验和
    icmp_chesksum = chesksum(imcp_packet)
    #  把校验和传入，再次打包
    imcp_packet = struct.pack('>BBHHH32s', data_type, data_code, icmp_chesksum, data_ID, data_Sequence, payload_body)
    return imcp_packet


# 初始化套接字，并发送
def raw_socket(dst_addr, imcp_packet):
    # 实例化一个socket对象，ipv4，原套接字(普通套接字无法处理ICMP等报文)，分配协议端口
    rawsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    # 记录当前请求时间
    send_request_ping_time = time.time()
    # 发送数据到网络
    rawsocket.sendto(imcp_packet, (dst_addr, 80))
    return send_request_ping_time, rawsocket


def reply_ping(send_request_ping_time, rawsocket, data_Sequence, timeout=2):
    while True:
        '''
        select函数，直到inputs中的套接字被触发（在此例中，套接字接收到客户端发来的握手信号，从而变得可读，满足select函数的“可读”条件），
        返回被触发的套接字（服务器套接字）；                
        '''
        # 实例化select对象（非阻塞），可读，可写为空，异常为空，超时时间
        what_ready = select.select([rawsocket], [], [], timeout)
        # 等待时间
        # wait_for_time = (time.time() - started_select)
        wait_for_time = (time.time() - send_request_ping_time)
        # 没有返回可读的内容，判断超时
        if what_ready[0] == []:  # Timeout
            return -1
        # 记录接收时间
        time_received = time.time()
        # 设置接收的包的字节为1024
        received_packet, addr = rawsocket.recvfrom(1024)
        # 获取接收包的icmp头
        # print(icmpHeader)
        icmpHeader = received_packet[20:28]
        # 反转编码
        type, code, r_checksum, packet_id, sequence = struct.unpack(
            ">BBHHH", icmpHeader
        )

        if type == 0 and sequence == data_Sequence:
            return time_received - send_request_ping_time

        # 数据包的超时时间判断
        timeout = timeout - wait_for_time
        if timeout <= 0:
            return -1


def dealtime(dst_addr, sumtime, shorttime, longtime, accept, i, time):
    sumtime += time
    print(sumtime)
    if i == 4:
        print("{0}的Ping统计信息：".format(dst_addr))
        print(
            "数据包：已发送={0},接收={1}，丢失={2}（{3}%丢失），\n往返行程的估计时间（以毫秒为单位）：\n\t最短={4}ms，最长={5}ms，平均={6}ms".format(i + 1, accept,
                                                                                                          i + 1 - accept,
                                                                                                          (
                                                                                                                      i + 1 - accept) / (
                                                                                                                      i + 1) * 100,
                                                                                                          shorttime,
                                                                                                          longtime,
                                                                                                          sumtime))


def ping(host):
    # 统计最终 已发送、 接受、 丢失
    send, accept, lost = 0, 0, 0
    sumtime, shorttime, longtime, avgtime = 0, 1000, 0, 0
    # TODO icmp数据包的构建
    # 8回射请求 11超时 0回射应答
    data_type = 8
    data_code = 0
    # 检验和
    data_checksum = 0
    # ID
    data_ID = 0
    # 序号
    data_Sequence = 1
    # 可选的内容
    payload_body = b'abcdefghijklmnopqrstuvwabcdefghi'  # data

    # 将主机名转ipv4地址格式，返回以ipv4地址格式的字符串，如果主机名称是ipv4地址，则它将保持不变
    dst_addr = socket.gethostbyname(host)
    print("正在 Ping {0} [{1}] 具有 32 字节的数据:".format(host, dst_addr))
    # 默认发送4次
    for i in range(0, 4):
        send = i + 1
        # 请求ping数据包的二进制转换
        icmp_packet = request_ping(data_type, data_code, data_checksum, data_ID, data_Sequence + i, payload_body)
        # 连接套接字,并将数据发送到套接字
        send_request_ping_time, rawsocket = raw_socket(dst_addr, icmp_packet)
        # 数据包传输时间
        times = reply_ping(send_request_ping_time, rawsocket, data_Sequence + i)
        if times > 0:
            print("来自 {0} 的回复: 字节=32 时间={1}ms".format(dst_addr, int(times * 1000)))

            accept += 1
            return_time = int(times * 1000)
            sumtime += return_time
            if return_time > longtime:
                longtime = return_time
            if return_time < shorttime:
                shorttime = return_time
            time.sleep(0.7)
        else:
            lost += 1
            print("请求超时。")

        if send == 4:
            print("{0}的Ping统计信息:".format(dst_addr))
            print("\t数据包：已发送={0},接收={1}，丢失={2}（{3}%丢失），\n往返行程的估计时间（以毫秒为单位）：\n\t最短={4}ms，最长={5}ms，平均={6}ms".format(
                i + 1, accept, i + 1 - accept, (i + 1 - accept) / (i + 1) * 100, shorttime, longtime, sumtime / send))


if __name__ == "__main__":
    # i = input("请输入要ping的主机或域名\n")
    i = "www.baidu.com"
    ping(i)
