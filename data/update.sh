#!/bin/bash
SCRIPT_PATH="${BASH_SOURCE[0]}";
if([ -h "${SCRIPT_PATH}" ]) then
  while([ -h "${SCRIPT_PATH}" ]) do SCRIPT_PATH=`readlink "${SCRIPT_PATH}"`; done
fi
SCRIPT_PATH=`dirname ${SCRIPT_PATH}`

cd $SCRIPT_PATH;





curl -X GET http://www.fresksite.net/dcadb/wp-content/themes/dca/api/iowans.php > _iowans.json
rm -r cache
mkdir -p cache
python sanitize.py