#!/bin/bash

PROJECT_PATH="/project/bbs"
source $PROJECT_PATH/.venv/bin/activate
gunicorn -c $PROJECT_PATH/bbs/gunicorn-config.py bbs.wsgi
