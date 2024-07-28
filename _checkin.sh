#!/bin/bash
if [[ "$1" == "" ]]; then
  COMMITMSG="checkpoint"
else
  COMMITMSG="$1"
fi
git add .
git commit -m "$COMMITMSG"
git push origin main
