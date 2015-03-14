#!/bin/bash
SCRIPT_PATH="${BASH_SOURCE[0]}";
if([ -h "${SCRIPT_PATH}" ]) then
  while([ -h "${SCRIPT_PATH}" ]) do SCRIPT_PATH=`readlink "${SCRIPT_PATH}"`; done
fi
SCRIPT_PATH=`dirname ${SCRIPT_PATH}`
cd $SCRIPT_PATH;

#cd ./data;
#./update.sh
#cd ..;

if [[ "$OSTYPE" == "darwin"* ]]; then
    KIVY_APP=${KIVYAPP:=/Applications/Kivy.app}
    ${KIVY_APP}/Contents/Resources/script ./main.py -m inspector --size=720x810 
else
    python ./main.py
fi