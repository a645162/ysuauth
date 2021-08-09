#!/bin/bash

base_directory="/ysuauth"

mode_file="$base_directory/mode.ysuauth"



#检测网络链接畅通
function network() {
  #超时时间
  local timeout=1

  #目标网站
  local target=www.gitee.com

  #获取响应状态码
  local ret_code=$(curl -I -s --connect-timeout ${timeout} ${target} -w %{http_code} | tail -n1)

  if [ "x$ret_code" = "x200" ]; then
    #网络畅通
    return 1
  else
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

# -f 参数判断 $file 是否存在
if [ -f "$mode_file" ]; then
  touch "mode_file"
fi

cat /dev/null >"$mode_file"

echo "test ddd sfafaf " >>"$mode_file"




# 判断是否已经Update
if [ ! -f "$BASE_PATH/git/ready.ysuauth" ]; then
  echo "检查时间："
  more "$BASE_PATH/git/check_date.ysuauth"
  echo "更新脚本执行完毕时间："
  more "$BASE_PATH/git/update_date.ysuauth"
fi

if [ "$mode" = "git" ]; then
  script_directory="$base_directory/git/allfiles/ysuauth_python/src"
else
  script_directory="$base_directory/src/"
fi


cd $script_directory || exit
python3 "autoauth.py"
