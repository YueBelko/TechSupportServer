#!/bin/bash
# ps aux
# kill
#
git clone https://YueBelko:Asakura31337@github.com/YueBelko/TechSupportServer.git
cd TechSupportServer
export FLASK_APP=run.py
export FLASK_DEBUG=1
# flask db migrate
# flask db upgrade
nohup flask run --host=0.0.0.0 > log.txt > /dev/null 2>&1 &