#!/bin/bash

set -e

echo "Start build"

time1=$(date "+%Y-%m-%d_%H-%M-%S")
echo "Start Time: $time1"

echo "Start Python Script"

sudo python mkimg.py

echo "Finished!"

time2=$(date "+%Y-%m-%d_%H-%M-%S")
echo "Start Time:  $time1"
echo "Finish Time: $time2"