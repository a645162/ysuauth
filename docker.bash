#!/usr/bin/env bash

set -e

time_now=$(date "+%Y-%m-%d_%H-%M-%S")
echo "Now Time: $time_now"

echo "Start build script"

chmod +x mkimg.sh
./mkimg.sh | tee "build_logs/mkimg_$time_now.log"
