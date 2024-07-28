#!/bin/bash

# install anaconda
#sudo apt-get install -y libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6

INSTALLER_VERSION="2024.06-1"
#curl -O https://repo.anaconda.com/archive/Anaconda3-${INSTALLER_VERSION}-Linux-x86_64.sh
#bash ./Anaconda3-${INSTALLER_VERSION}-Linux-x86_64.sh
source ~/anaconda3/bin/activate
conda init
conda config --set auto_activate_base False
