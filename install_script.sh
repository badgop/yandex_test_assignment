#!/bin/bash
#не забыть дать права на исполнения chmod +x setup_vcan.sh
#настояший скрипт необходим для установки необходимых пакетов на чистую ОС (Ubuntu 20.04)
#****************************
sudo apt install can-utils
sudo apt install wireshark
#для проверки наличия интфейрсов vcan в консоли через ifconfig
sudo apt install net-tools

echo "Done...."