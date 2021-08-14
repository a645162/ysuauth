#!/bin/bash

#isUpdate=$([ "aa" = "aa" ])

[ "aa" = "aa" ] && isUpdate=true || isUpdate=false

if [ "$isUpdate" = true ];then
  echo "1"
else
  echo "2"
fi