#!/bin/bash




#检测网络链接畅通
network() {
  #超时时间
  local timeout=1

  #目标网站
  local target=www.gitee.com

  echo "curl -I -s --connect-timeout ${timeout} ${target} -w %{http_code}"

  curl -I -s --connect-timeout "${timeout}" "${target}" -w "%{http_code}" | tail -n1

  #获取响应状态码
  local ret_code
  ret_code="$(curl -I -s --connect-timeout "${timeout}" "${target}" -w "%{http_code}" | tail -n1)"
#  echo "$ret_code" >>"$mode_file"
  echo "$ret_code"

  #curl -I -s --connect-timeout 1 www.gitee.com -w "%{http_code}" | tail -n1

  if [ "$ret_code" = "301" ]; then
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

if network; then
  mode="git"
else
  mode="local"
fi

echo $mode


if ! ping -c 5 "www.gitee.com"; then
  echo " can not connect "
else
  echo "ok"
fi
