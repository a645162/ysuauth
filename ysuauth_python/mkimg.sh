#!/usr/bin/env bash
docker buildx build --platform linux/amd64,linux/arm64,linux/386 -t a645162/ysuauth:1.0 .
docker build -t a645162/ysuauth:1.0 .

#docker buildx build -t yangchuansheng/hello-arch --platform=linux/arm,linux/arm64,linux/amd64 . --push