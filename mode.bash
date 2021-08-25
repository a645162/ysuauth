#!/bin/bash

[ -f "$BASE_PATH/remote/ready.ysuauth" ] && isUpdate=true || isUpdate=false

#检测网络链接畅通
network() {
  #超时时间
  local timeout=1

  #目标网站
  local target=www.baidu.com

  echo "curl -I -s --connect-timeout ${timeout} ${target} -w %{http_code}"
  #获取响应状态码

  local ret_code
  ret_code="$(curl -I -s --connect-timeout "${timeout}" "${target}" -w "%{http_code}" | tail -n1)"
  #  echo "$ret_code" >>"$mode_file"
  echo "$target return $ret_code"

  #curl -I -s --connect-timeout 1 www.gitee.com -w %{http_code} | tail -n1

  if [ "$ret_code" = "200" ]; then
    echo "Connect $target Ok!"
    #网络畅通
    return 0
  else
    echo "Fail to connect to $target!"
    #网络不畅通
    return 1
  fi

  return 1
}

echo "isUpdate = $isUpdate"

# 判断是否已经Update
if [ "$isUpdate" = true ]; then
  echo "Check Time："
  more "$BASE_PATH/remote/check_date.ysuauth"
  echo "Last end time："
  more "$BASE_PATH/remote/update_date.ysuauth"
  mode="git"
else
  echo "还未clone仓库"
  mode="local"

  if [ "$USE_DEFAULT_GIT" = "True" ]; then
    echo "设置->默认使用Git版本"
    if network; then
      echo "联网状态->已经连接到互联网！"
      echo "Update脚本->前台阻塞执行Update！"

      if python3 "update.py" -i; then
        mode="git"
      else
        mode="local"
      fi
      [ -f "$BASE_PATH/remote/ready.ysuauth" ] && isUpdate=true || isUpdate=false
      if [ "$isUpdate" = true ]; then
        echo "Update脚本->更新完毕！"
        mode="git"
      else
        echo "Update脚本->更新失败！"
        echo "Update脚本->后台静默等待网络并执行Update！"
        python3 "update.py" -w &
        mode="local"
      fi
    else
      echo "联网状态->还未连接到互联网！"
      echo "Update脚本->后台静默等待网络并执行Update！"
      python3 "update.py" -w &
      mode="local"
    fi
  fi

fi

echo "mode = $mode"

if ! ping -c 5 www.gitee.com; then
  echo "Can't ping to www.gitee.com"
  mode="local"
fi

if [ ! "$USE_DEFAULT_GIT" = "True" ] || [ ! "$mode" = "git" ]; then
  mode="local"
fi

echo "mode.bash = $mode"

if [ "$mode" = "git" ]; then
  exit 0
else
  exit 1
fi
