FROM python:3.11.4-alpine3.18
MAINTAINER Haomin Kong

LABEL AUTHOR="Haomin Kong" \
      VERSION=3

WORKDIR /ysuauth

# FROM # 基础镜像 比如node
# MAINTAINER # 镜像是谁写的 姓名+邮箱(MAINTAINER已经被废弃)
# LABEL # 给镜像添加一些元数据
# ARG # 构建参数,与 ENV 作用一至.不过作用域不一样。ARG设置的环境变量仅对Dockerfile内有效,也就是说只有docker build的过程中有效，构建好的镜像内不存在此环境变量
# RUN # 镜像构建时需要运行的命令
# ADD # 添加，比如添加一个tomcat压缩包
# WORKDIR # 镜像的工作目录
# VOLUME # 挂载的目录
# EXPOSE # 指定暴露端口，跟-p一个道理
# RUN # 最终要运行的
# CMD # 指定这个容器启动的时候要运行的命令，只有最后一个会生效，而且可被替代
# ENTRYPOINT # 指定这个容器启动的时候要运行的命令，可以追加命令
# ONBUILD # 当构建一个被继承Dockerfile 这个时候运行ONBUILD指定，触发指令
# COPY # 将文件拷贝到镜像中
# ENV # 构建的时候设置环境变量

# ====================================================================
# Add proxy, using --build-arg "HTTP_PROXY=http://192.168.1.112:7890"

# set -e ： -e这个参数的含义是,当命令发生错误的时候,停止脚本的执行
# set -x ： -x参数的作用是把将要运行的命令用一个+标记之后显示出来
# echo -e ：激活转义字符
# echo -n ：不换行输出
# apk : 软件包管理工具
# mkdir -p ：递归创建目录，即使上级目录不存在，会按目录层级自动创建目录
# git clone -b : 克隆指定的分支 git clone -b 分支名 仓库地址

ENV DOCKER="Haomin Kong" \
    BASE_PATH="/ysuauth" \
    REPO_URL="https://gitee.com/yskoala/ysuauth.git" \
#    REPO_BRANCH="develop"
    REPO_BRANCH="beta"
#    REPO_BRANCH="master"

#ENV USE_DEFAULT_GIT="True"
#这俩有很大的区别啊！坑死我了！
#ENV USE_DEFAULT_GIT = "True"

ENV LOGS_PATH="/ysuauth/logs" \
    SETTINGS_PATH="/ysuauth/settings"

# 燕大我觉得速度最快的就是清华源了！
RUN echo "[global] \
    index-url = https://pypi.tuna.tsinghua.edu.cn/simple \
    trusted-host = pypi.tuna.tsinghua.edu.cn \
    timeout = 120 \
    " > /etc/pip.conf \
    && sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    && apk add --no-cache build-base libffi-dev tzdata bash \
    && apk add --no-cache git curl \
    # 我觉得吧，还是比较有必要用清华源的。 \
    && pip3 --no-cache-dir install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U \
    && pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip3 --no-cache-dir install ping3 ntplib requests GitPython python-dateutil \
    && rm -rf ~/.cache/pip \
    && rm -rf /tmp/* \
    && apk del libffi-dev build-base \
#    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo Haomin Kong >> docker_status \
    && echo "Asia/Shanghai" > /etc/timezone

# 主要目的还是拷贝update.py
# 主要是这里面的耦合太复杂了，都拷贝了吧！
COPY src/*.py /ysuauth/
COPY src/*.sh /ysuauth/
COPY src/*.bash /ysuauth/

COPY src/*.py /ysuauth/src/
COPY src/*.sh /ysuauth/src/
COPY src/*.bash /ysuauth/
COPY src/*.list /ysuauth/src/

COPY *.sh /ysuauth/
COPY *.bash /ysuauth/

RUN find /ysuauth/ -name '*.sh' -type f -print -exec chmod +x {} \;
RUN find /ysuauth/ -name '*.bash' -type f -print -exec chmod +x {} \;

RUN rm -rf /ysuauth/src/logs; exit 0 \
    && rm -rf /ysuauth/src/settings; exit 0 \
    && rm -rf /ysuauth/src/remote; exit 0 \
    && rm -f /ysuauth/src/*.ysuauth; exit 0

RUN    mkdir $LOGS_PATH; exit 0 \
    && mkdir $SETTINGS_PATH; exit 0 \
    && chmod -R 777 $LOGS_PATH

# RUN #python3 ntp_hosts.py

ENV GIT_ENV="GIT" \
    USE_DEFAULT_GIT="True"
#ENV DEBUG="True"
#ENV IGNORE_WORK_TIME="True"

ENTRYPOINT ["/ysuauth/entrypoint.sh"]