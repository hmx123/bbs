#!/bin/bash

PROJECT_PATH="/project/bbs"
echo "stop gunicorn"
$PROJECT_PATH/scripts/stop.sh   # 终止进程

sleep 1s  # 等待 1s 确保 gunicorn 已终止

echo "start gunicorn"
$PROJECT_PATH/scripts/start.sh  # 启动 gunicorn
