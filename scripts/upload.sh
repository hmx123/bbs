#!/bin/bash
# 文件上传脚本

SERVER_USER="root"
SERVER_IP="35.194.171.19"
SERVER_PATH="/project/bbs/"

rsync -crvP --exclude={.venv,.git,__pycache__,*.log,*.pid} ./ $SERVER_USER@$SERVER_IP:$SERVER_PATH
