#!/bin/bash

#set -e



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

#检测网络链接畅通
network() {
  #超时时间
  timeout=1

  #目标网站
  target=www.gitee.com

  #获取响应状态码
  ret_code=$(curl -I -s --connect-timeout ${timeout} ${target} -w %{http_code} | tail -n1)
  echo "$ret_code" >>"$mode_file"

  if [ "$ret_code" = "200" ]; then
    echo "Connect www.gitee.com Ok!"
    #网络畅通
    return 1
  else
    echo "Fail to connect to www.gitee.com!"
    #网络不畅通
    return 0
  fi

  return 0
}

network
if [ $? -eq 0 ]; then
  mode="git"
else
  mode="local"
fi

# 判断是否已经Update
if [ ! -f "$BASE_PATH/git/ready.ysuauth" ]; then
  echo "Check Time："
  more "$BASE_PATH/git/check_date.ysuauth"
  echo "Last end time："
  more "$BASE_PATH/git/update_date.ysuauth"
else
  if [ "$USE_DEFAULT_GIT" = "True" ]; then
    python3 "update.py" &
  fi
  mode="local"
fi

if [ ! "$USE_DEFAULT_GIT" = "True" ] || [ ! "$mode" = "git" ]; then
  mode="local"
fi

if [ "$mode" = "git" ]; then
  script_directory="$base_directory/git/allfiles/ysuauth_python/src"
else
  script_directory="$base_directory/src/"
fi

cd $script_directory || exit
python3 "autoauth.py"
cd $base_directory || exit
python3 "update.py"

reboot
