#!/bin/sh
set -e

#获取配置的自定义参数
#if [ $1 ]; then
#    run_cmd=$1
#fi

echo "set remote git url..."
git clone https://gitee.com/a645162/ysuauth.git /ysuauth
cd /ysuauth
git remote set-url origin $REPO_URL
git reset --hard
git branch -u $REPO_BRANCH
echo "pull code from gitee"
git -C /ysuauth pull --rebase

git clone -b develop https://gitee.com/a645162/ysuauth.git /ysuauth

echo "--------start--------"
cd /ysuauth
/usr/local/bin/python3 autoauth.py
