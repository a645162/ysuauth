#!/bin/bash

#set -e

sudo docker build -f "Dockerfile_git" --load \
  -t a645162/ysuauth-test:latest .
