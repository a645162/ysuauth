FROM python:3.9.6-alpine
MAINTAINER Haomin Kong

LABEL AUTHOR = "Haomin Kong" \
      VERSION = 1

WORKDIR /ysuauth

ENV REPO_URL="https://gitee.com/a645162/ysuauth.git" \
    REPO_BRANCH="develop"
    #REPO_BRANCH=master


RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk add --no-cache build-base libffi-dev git \
#    && apk add -U --no-cache tzdata \
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
    && echo "Asia/Shanghai" > /etc/timezone \
    && python3 ntp_hosts.py
#    && chronyd

#COPY entrypoint.sh entrypoint.sh
COPY src/ /ysuauth
RUN rm -rf /ysuauth/gitversion/allfiles

#ENTRYPOINT ["entrypoint.sh"]
CMD python3 autoauth.py