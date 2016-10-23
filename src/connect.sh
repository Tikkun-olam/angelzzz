#!/bin/bash
SCRIPT_PATH=$(dirname $(realpath -s $BASH_SOURCE))
MAC=$(<${SCRIPT_PATH}/beddit_mac.txt)
$SCRIPT_PATH/beddit_connect ${MAC}
$SCRIPT_PATH/bind.sh ${MAC}
