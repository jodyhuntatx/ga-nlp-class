#!/bin/bash
pip3 install notebook ipywidgets
cd ..
echo "Detach: 'Ctrl-b d'"
echo "Attach: 'tmux attach -t jupyter"
read -n 1 -s -r -p "Press any key to continue"
tmux new -s jupyter jupyter notebook --no-browser --port=3000 --ServerApp.ip=0.0.0.0
