#!/bin/bash

docker buildx install

# alpine支持的所有platform我都支持一下吧(3.9.6-alpine3.13有linux/s390x而3.14就没了，就不支持了)

docker buildx build --push \
  --platform linux/amd64,linux/arm64,linux/386,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x \
  -t a645162/ysuauth:3.0.2 .

#docker build -t ysuauth-dev:3.0.2 .

#docker buildx build -t yangchuansheng/hello-arch --platform=linux/arm,linux/arm64,linux/amd64 . --push
