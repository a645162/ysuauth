#!/bin/bash

sudo apt-get install ntp

ntp_service=$(
  cat <<EOF

server cn.ntp.org.cn prefer
server ntp.ntsc.ac.cn prefer
server ntp.bupt.edu.cn prefer
server time2.apple.com prefer
# server 0.debian.pool.ntp.org iburst
# server 1.debian.pool.ntp.org iburst
# server 2.debian.pool.ntp.org iburst
# server 3.debian.pool.ntp.org iburst
server time.asia.apple.com prefer
server ntp.sjtu.edu.cn prefer
# server 127.127.1.0
# fudge 127.127.1.0 stratum 10
EOF
)

#rm -f /etc/docker/daemon.json
echo "$ntp_service" | sudo tee -a /etc/ntp.conf

sudo service ntp restart

ps -ef | grep ntp

ntpq -p
