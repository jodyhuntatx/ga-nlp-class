#!/bin/bash
pip3 install notebook ipywidgets
cd ..
tmux -s jupyter jupyter notebook --no-browser --port=3000 --ServerApp.ip=0.0.0.0
