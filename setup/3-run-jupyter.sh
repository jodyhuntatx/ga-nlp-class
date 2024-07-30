#!/bin/bash
echo "Detach: 'Ctrl-b d'"
echo "Attach: 'tmux attach -t jupyter"
read -n 1 -s -r -p "Press any key to continue"
cd ~
tmux new -s jupyter jupyter notebook --no-browser --port=3000 --ServerApp.ip=0.0.0.0
