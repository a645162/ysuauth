"""
2023年7月15日

编写本脚本主要为了解决 Windows 环境下编译困难的问题！
本脚本将代替 mkimg.sh
"""

import datetime
import os
import re
import sys

need_run = True


def exe_command(command):
    out = os.popen(command)
    return str(out.readlines()[0]).strip()


def run_sh(command):
    if need_run:
        os.system(command)


def generate_command(dockerfile_path='Dockerfile', branch='master', version='latest', option="", replace_text=None,
                     run=False):
    platform = "linux/amd64,linux/arm64,linux/386,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x"

    tag = ""

    # 这个仓库是我用的，建议您手动配置您的阿里云 容器镜像服务！
    # 一定，一定，一定要删除我的，否则会推送失败的哦！
    remote_warehouses = [
        "a645162/ysuauth",
        # "a645162/ysuauth-dev",
        # "registry.cn-zhangjiakou.aliyuncs.com/yskoala/ysuauth",
        # "registry.cn-zhangjiakou.aliyuncs.com/yskoala/ysuauth-dev",
    ]

    # option

    # branch = "master"
    for remote_warehouse in remote_warehouses:
        start_str = "            " + "-t "
        if branch == "master":
            if len(option) > 0:
                tag += start_str + remote_warehouse + f":{option}-latest" + " \\\n"
                tag += start_str + remote_warehouse + f":{option}-{version}" + " \\\n"
            else:
                tag += start_str + remote_warehouse + ":latest" + " \\\n"
                tag += start_str + remote_warehouse + f":{version}" + " \\\n"
        else:
            if len(option) > 0:
                tag += start_str + remote_warehouse + f":{branch}-{option}-latest" + " \\\n"
                tag += start_str + remote_warehouse + f"-{branch}:{option}-latest" + " \\\n"

                # 只在测试版将版本号上传到主仓库
                if branch == "beta":
                    tag += start_str + remote_warehouse + f":{branch}-{option}-{version}" + " \\\n"
                    tag += start_str + remote_warehouse + f"-{branch}:{option}-{version}" + " \\\n"
            else:
                tag += start_str + remote_warehouse + f":{branch}-latest" + " \\\n"
                tag += start_str + remote_warehouse + f"-{branch}:latest" + " \\\n"

                # 只在测试版将版本号上传到主仓库
                if branch == "beta":
                    tag += start_str + remote_warehouse + f":{branch}-{version}" + " \\\n"
                    tag += start_str + remote_warehouse + f"-{branch}:{version}" + " \\\n"

    tag = tag.strip()
    if len(tag) > 0:
        tag += "\n"

    with open(os.path.join(current_dir, 'build_command_line.sh'), 'r') as f:
        build_command = f.read().strip()

    if replace_text is not None:
        for k in replace_text.keys():
            print(k)
            build_command = re.sub(k, replace_text[k], build_command)

    build_command = build_command.format(dockerfile_path, platform, tag).strip()

    print(build_command)
    print("即将调用buildx构建镜像")
    run_sh(build_command)


if __name__ == '__main__':

    for i in range(1, len(sys.argv)):
        parm = sys.argv[i].strip()
        if parm == 'donotrun':
            need_run = False

    current_dir = os.path.dirname(os.path.abspath(__file__))

    branch = exe_command(r"git branch | sed -n '/\* /s///p'").strip()
    if branch == 'develop':
        branch = 'dev'

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
    run_sh("docker login")

    # print("\n" * 3)
    # print("请登录阿里云账号(Docker仓库有独立密码)")
    # # 登录 阿里云 Docker 仓库
    # run_sh("docker login --username=a645162@qq.com registry.cn-zhangjiakou.aliyuncs.com")

    # 初始化 buildx
    print("--" * 10)
    print("初始化 buildx")
    run_sh("docker buildx install")
    print("--" * 10)

    print("生成远程版")
    generate_command(
        branch=branch,
        version=version,
        replace_text={
            r'\$\{GIT_ENV}': 'GIT',
            r'\$\{USE_DEFAULT_GIT}': 'True'
        }
    )
    print("--" * 10)

    print("生成本地版")
    generate_command(
        branch=branch,
        version=version,
        option="local",
        replace_text={
            r'\$\{GIT_ENV}': 'LOCAL',
            r'\$\{USE_DEFAULT_GIT}': 'False'
        }
    )

    print("--" * 10)

    end_time = datetime.datetime.now()
    print("Python Finished Time:", end_time)
    print("Used Time:", end_time - start_time)
