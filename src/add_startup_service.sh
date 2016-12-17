INSTALL_PATH=$(realpath $(dirname $0))
SCRIPT_PATH=${INSTALL_PATH}/config/angelzzz.service
EXEC_PATH=${INSTALL_PATH}/angelzzz_server.py
LOG_PATH=${INSTALL_PATH}/stdout.log

sudo cp ${SCRIPT_PATH} /etc/systemd/system/angelzzz.service
sudo sed -i 's@SERVER_PLACEHOLDER@'"$EXEC_PATH"'@g' /etc/systemd/system/angelzzz.service
sudo sed -i 's@LOG_PLACEHOLDER@'"$LOG_PATH"'@g' /etc/systemd/system/angelzzz.service
sudo sed -i 's@WORKING_DIR_PLACEHOLDER@'"$INSTALL_PATH"'@g' /etc/systemd/system/angelzzz.service

sudo systemctl daemon-reload
sudo systemctl enable angelzzz.service
sudo systemctl stop angelzzz.service
sudo systemctl start angelzzz.service
