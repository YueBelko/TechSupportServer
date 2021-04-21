#!/bin/bash
cd /home/user/techsupport
export FLASK_APP=run.py
export FLASK_DEBUG=1
flask run --host=0.0.0.0 > log.txt > /dev/null 2>&1 &