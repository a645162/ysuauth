#!/bin/bash

#set -e

bit=$(getconf LONG_BIT)

echo "bit=$bit"

if [ ! -a ~/bit.txt ]; then
  echo "bit=$bit" >~/bit.txt
fi

if [ "$bit" = "64" ]; then
  arch="arm64"
else
  arch="armhf"
  echo "温馨提醒：32位树莓派系统需要更新补丁！"
fi

echo "USE_DEFAULT_GIT = $USE_DEFAULT_GIT"

base_directory="/ysuauth"
if [ "$DOCKER" = "Haomin Kong" ]; then
  base_directory="/ysuauth"
else
  base_directory=$(pwd)
fi

#mode_file="$base_directory/log/mode.ysuauth"
mode_file="$LOGS_PATH/mode.ysuauth"

# -f 参数判断 $file 是否存在
if [ -f "$mode_file" ]; then
  touch "mode_file"
fi

# cat /dev/null > "$mode_file"
echo "( $(date "+%Y-%m-%d %H:%M:%S") ) RUN entrypoint" >>"$mode_file"

if [ "$GIT_ENV" = "GIT" ]; then
  chmod 777 mode.bash
  if ./mode.bash; then
    mode="git"
  else
    mode="local"
  fi
else
  echo "!!!Local Build!!!"
  echo "!!!Local Build!!!"
  echo "!!!Local Build!!!"
  mode="local"
fi

if [ "$mode" = "git" ]; then
  echo "最终决定！Git模式！"
  echo "[git仓库目录结构类型]新版目录结构！"
  if [ ! -d ""$base_directory/remote/allfiles/src"" ]; then
    script_directory="$base_directory/remote/allfiles/src"
  else
    echo "[git仓库目录结构类型]旧版目录结构！"
    script_directory="$base_directory/remote/allfiles/ysuauth_python/src"
  fi
else
  echo "最终决定！Local模式！"
  script_directory="$base_directory/src"
fi

echo "脚本文件路径$script_directory"

cd "$script_directory" || exit
python3 "auto_auth.py"
cd "$base_directory" || exit
python3 "update.py"

reboot
