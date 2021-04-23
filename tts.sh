#!/bin/bash
# ps aux
# kill
#
FFF= `ps aux | grep '/usr/local/bin/flask' | cut -d ' ' -f7`
for F in $FFF
do
  echo $F
done;
rm -R TechSupportServer
git clone https://YueBelko:Asakura31337@github.com/YueBelko/TechSupportServer.git
cd TechSupportServer
export FLASK_APP=run.py
export FLASK_DEBUG=1
# flask db migrate
# flask db upgrade
nohup flask run --host=0.0.0.0 > log.txt > /dev/null 2>&1 &

# cp tts.sh ../tts.sh
# chmod u+x tts.sh