#!/bin/bash

base_directory="/ysuauth"

mode_file="$base_directory/mode.ysuauth"

script_directory="$base_directory/src/"
script_directory="$base_directory/gitversion/allfiles/ysuauth_python/src"

# -f 参数判断 $file 是否存在
if [ -f "$mode_file" ]; then
  touch "$file"
fi

script_path="$script_directory/autoauth.py"

python3 $script_path