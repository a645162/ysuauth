#!/bin/bash

set -e

echo "Start build"

time1=$(date "+%Y-%m-%d_%H-%M-%S")
echo "Start Time: $time1"

echo "接下来登录 Docker Hub 官方"
docker login

echo "接下来登录阿里云Docker"
docker login --username=a645162@qq.com registry.cn-zhangjiakou.aliyuncs.com

docker buildx install
rm -f src/*.log

# !!!!alpine支持的所有platform我都支持一下吧(3.9.6-alpine3.13有linux/s390x而3.14就没了，就不支持了)
# 我觉得，顺带带上linux/s390x得了。

version="4.0.1"
branch=""
#branch="master"
#branch="beta"
branch="dev"

if [ ! "$branch" = "" ]; then
  branch_str="$branch-"
  branch_str_front="-$branch"
fi

echo "即将开始build git version v$version"

if [ ! -f "Dockerfile_git" ]; then
  echo "找不到 Dockerfile_git"
  cp Dockerfile Dockerfile_git
fi
if [ "$branch" = "dev" ]; then
  docker buildx build -f "Dockerfile_git" --push \
    --build-arg GIT_ENV="GIT" \
    --build-arg USE_DEFAULT_GIT="True" \
    --progress=plain --no-cache \
    --platform linux/amd64,linux/arm64,linux/386,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x \
    -t a645162/ysuauth${branch_str_front}:${version} \
    -t a645162/ysuauth${branch_str_front}:latest \
    -t registry.cn-zhangjiakou.aliyuncs.com/yskoala/ysuauth${branch_str_front}:${version} \
    -t registry.cn-zhangjiakou.aliyuncs.com/yskoala/ysuauth${branch_str_front}:latest \
    -t registry.cn-zhangjiakou.aliyuncs.com/yskoala/ysuauth:${branch_str}latest \
    -t a645162/ysuauth:${branch_str}latest .
#    -t a645162/ysuauth:${branch_str}v${version} \
else
  docker buildx build -f "Dockerfile_git" --push \
    --build-arg GIT_ENV="GIT" \
    --build-arg USE_DEFAULT_GIT="True" \
    --progress=plain --no-cache \
    --platform linux/amd64,linux/arm64,linux/386,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x \
    -t registry.cn-zhangjiakou.aliyuncs.com/yskoala/ysuauth:${branch_str}${version} \
    -t registry.cn-zhangjiakou.aliyuncs.com/yskoala/ysuauth:${branch_str}latest \
    -t a645162/ysuauth:${branch_str}${version} \
    -t a645162/ysuauth:${branch_str}latest .
#    -t a645162/ysuauth${branch_str_front}:v${version} -t a645162/ysuauth${branch_str_front}:latest \
fi

echo ""
echo "即将开始build local version v$version"

if [ ! -f "Dockerfile_git" ]; then
  echo "找不到 Dockerfile_git"
  cp Dockerfile_git Dockerfile_local
fi

if [ "$branch" = "dev" ]; then
  docker buildx build -f "Dockerfile_local" --push \
    --build-arg GIT_ENV="LOCAL" \
    --build-arg USE_DEFAULT_GIT="False" \
    --progress=plain --no-cache \
    --platform linux/amd64,linux/arm64,linux/386,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x \
    -t a645162/ysuauth${branch_str_front}:local-${version} \
    -t a645162/ysuauth${branch_str_front}:local-latest \
    -t registry.cn-zhangjiakou.aliyuncs.com/yskoala/ysuauth${branch_str_front}:local-${version} \
    -t registry.cn-zhangjiakou.aliyuncs.com/yskoala/ysuauth${branch_str_front}:local-latest \
    -t registry.cn-zhangjiakou.aliyuncs.com/yskoala/ysuauth:${branch_str}local-latest \
    -t a645162/ysuauth:${branch_str}local-latest .
#    -t a645162/ysuauth:${branch_str}local-v${version} \
else
  docker buildx build -f "Dockerfile_local" --push \
    --build-arg GIT_ENV="LOCAL" \
    --build-arg USE_DEFAULT_GIT="False" \
    --progress=plain --no-cache \
    --platform linux/amd64,linux/arm64,linux/386,linux/arm/v7,linux/arm/v6,linux/ppc64le,linux/s390x \
    -t a645162/ysuauth:${branch_str}local-${version} \
    -t a645162/ysuauth:${branch_str}local-latest \
    -t registry.cn-zhangjiakou.aliyuncs.com/yskoala/ysuauth:${branch_str}local-${version} \
    -t registry.cn-zhangjiakou.aliyuncs.com/yskoala/ysuauth:${branch_str}local-latest .
#  -t a645162/ysuauth${branch_str_front}:local-v${version} -t a645162/ysuauth${branch_str_front}:local-latest \
fi

echo "Finished!"

time2=$(date "+%Y-%m-%d_%H-%M-%S")
echo "Start Time:  $time1"
echo "Finish Time: $time2"

#docker tag ysuauth:${version} a645162/ysuauth:${version}

#docker tag a645162/ysuauth:${version} a645162/ysuauth:latest
#docker tag a645162/ysuauth:3.0.3 a645162/ysuauth:latest
#docker push ysuauth/ysuauth:latest

#docker build -t ysuauth-dev:3.0.3 -t ysuauth:3.0.3 .

#docker build -t a645162/ysuauth-dev:local-latest -f "Dockerfile_local" --push .
