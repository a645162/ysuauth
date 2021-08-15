#!/bin/bash

# 这个问题只会出现在Armhf，也就是32位的树莓派系统上(树莓派4虽然是64位处理器，但是也是可以安装32位系统的)

#based on https://docs.linuxserver.io/faq#my-host-is-incompatible-with-images-based-on-ubuntu-focal-and-alpine-3-13

# 我比较推荐解决方案1，因为这个不用修改源。

# 解决方案1：
wget http://ftp.us.debian.org/debian/pool/main/libs/libseccomp/libseccomp2_2.4.4-1~bpo10+1_armhf.deb
sudo dpkg -i libseccomp2_2.4.4-1~bpo10+1_armhf.deb

# 解决方案2：
#sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC 648ACFD622F3D138
#echo "deb http://deb.debian.org/debian buster-backports main" | sudo tee -a /etc/apt/sources.list.d/buster-backports.list
#sudo apt update
#sudo apt install -t buster-backports libseccomp2
