#!/bin/bash

PROJECT_PATH="/project/bbs"
GUNICORN_PID=`cat $PROJECT_PATH/gunicorn.pid`
kill -15 $GUNICORN_PID
