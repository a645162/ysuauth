"""
2023年7月15日

编写本脚本主要为了解决 Windows 环境下编译困难的问题！
本脚本将代替 mkimg.sh
"""

import datetime
import os


def exe_command(command):
    out = os.popen(command)
    return str(out.readlines()[0]).strip()


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))

    branch = exe_command(r"git branch | sed -n '/\* /s///p'")

    with open(os.path.join(current_dir, "version"), 'r') as f:
        version = f.read().strip()

    print("--" * 10)
    print("YsuAuth Docker image builder(Python)")
    print("Version", version)
    print("Branch", branch)
    print("--" * 10)
    start_time = datetime.datetime.now()
    print("Now time:", start_time)
    print("--" * 10)


    # 登录 Docker 官方
    print("请登录官方Docker Hub")
    os.system("docker login")

    print("\n"*3)
    print("请登录阿里云账号(Docker仓库有独立密码)")
    # 登录 阿里云 Docker 仓库
    os.system("docker login --username=a645162@qq.com registry.cn-zhangjiakou.aliyuncs.com")

    # 初始化 buildx
    os.system("docker buildx install")


    build_command = \
        """
        
        """

    # os.system("ping www.baidu.com")

    end_time = datetime.datetime.now()
    print("Python Finished Time:", end_time)
    print("Used Time:", end_time - start_time)
