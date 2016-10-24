#!/bin/bash
SCRIPT_PATH=$(dirname $(realpath -s $BASH_SOURCE))
MAC=$(<${SCRIPT_PATH}/beddit_mac.txt)
if [ -f /dev/rfcomm0 ]; then
    sudo rfcomm release /dev/rfcomm0
fi
while [[ `hcitool scan` != *"${MAC}"* ]]; do  echo "searching" ; sleep 1; done


#$SCRIPT_PATH/beddit_connect ${MAC}
sudo rfcomm release /dev/rfcomm0
$SCRIPT_PATH/bind.sh ${MAC}
