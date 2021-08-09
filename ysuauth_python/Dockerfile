FROM python:3.9.6-alpine
MAINTAINER Haomin Kong

LABEL AUTHOR = "Haomin Kong" \
      VERSION = 2

WORKDIR /ysuauth

ENV DOCKER="Haomin Kong"

ENV BASE_PATH="/ysuauth"

ENV REPO_URL="https://gitee.com/a645162/ysuauth.git"
ENV REPO_BRANCH="develop"
#ENV REPO_BRANCH=master

ENV USE_DEFAULT_GIT = "True"

ENV DOCKER="You are right!"

ENV LOGS_PATH="/ysuauth/logs"
ENV SETTINGS_PATH="/ysuauth/settings"

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk add --no-cache build-base libffi-dev git \
    # 我觉得吧，还是比较有必要用清华源的。
    && pip --no-cache-dir install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
#    && /usr/local/bin/python -m pip --no-cache-dir install --upgrade pip \
    && pip --no-cache-dir install ping3 ntplib requests \
    && rm -rf ~/.cache/pip \
    && rm -rf /tmp/* \
#    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && apk del libffi-dev build-base \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo Haomin Kong >> docker_status \
    && echo "Asia/Shanghai" > /etc/timezone

COPY src/getenv.py /ysuauth/getenv.py
COPY entrypoint.sh entrypoint.sh
COPY src/ /ysuauth/src

RUN rm -rf /ysuauth/src/git
RUN rm -rf /ysuauth/src/logs
RUN rm -rf /ysuauth/src/git
#RUN mkdir /ysuauth/src/logs
RUN chmod -R 777 /ysuauth/src/logs

RUN mv /ysuauth/src/update.* /ysuauth/
RUN rm -rf *restart.ysuauth

RUN git clone -b $REPO_BRANCH $REPO_URL

RUN python3 ntp_hosts.py

ENTRYPOINT ["entrypoint.sh"]
#CMD python3 autoauth.py