#!/bin/bash

set -e

#docker buildx install

# alpine支持的所有platform我都支持一下吧(3.9.6-alpine3.13有linux/s390x而3.14就没了，就不支持了)

version="4.0.0"
branch=""
#branch="master"
branch="dev"

if [ ! "$branch" = "" ]; then
  branch_str="$branch-"
  branch_str_front="-$branch"
fi


#docker buildx build --push \
#  --progress=plain --no-cache \
#  --platform linux/amd64,linux/arm64,linux/386,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x \
#  -t a645162/ysuauth:${version} .

#docker tag ysuauth:${version} a645162/ysuauth:${version}

#docker tag a645162/ysuauth:${version} a645162/ysuauth:latest
#docker tag a645162/ysuauth:3.0.3 a645162/ysuauth:latest
#docker push ysuauth/ysuauth:latest

echo "a645162/ysuauth${branch_str_front}:local-${version}"
echo "registry.cn-zhangjiakou.aliyuncs.com/yskoala/ysuauth${branch_str_front}:local-${version}"
echo "a645162/ysuauth:${branch_str}local-latest"

#a645162/ysuauth-dev:local-4.0.0
#a645162/ysuauth:dev-local-4.0.0
#registry.cn-zhangjiakou.aliyuncs.com/yskoala/ysuauth-dev:local-4.0.0


docker buildx build -f "Dockerfile_local" --push \
    --build-arg GIT_ENV="LOCAL" \
    --build-arg USE_DEFAULT_GIT="False" \
    --progress=plain --no-cache \
    --platform linux/amd64,linux/arm64,linux/386,linux/arm/v7,linux/arm/v6 \
    -t a645162/ysuauth${branch_str_front}:local-${version} \
    -t a645162/ysuauth:${branch_str}local-${version} .
#    -t registry.cn-zhangjiakou.aliyuncs.com/yskoala/ysuauth${branch_str_front}:local-${version} \

#docker build -t ysuauth-dev:${version} .

#docker-compose --compatibility -f docker-compose-test.yml up -d
