
FROM python:3.9.4-alpine
MAINTAINER Haomin Kong

LABEL AUTHOR = "Haomin Kong" \
      VERSION = 1

ENV REPO_URL=https://gitee.com/a645162/ysuauth.git \
    REPO_BRANCH=develop
    #REPO_BRANCH=master

RUN apk add --no-cache build-base libffi-dev \
 && pip --no-cache-dir install urllib requests \
 && rm -rf ~/.cache/pip \
 && rm -rf /tmp/* \
 && apk del libffi-dev build-base
 && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
 && echo "Asia/Shanghai" > /etc/timezone \

COPY entrypoint.sh entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]