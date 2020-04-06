#!/bin/bash
VIRTUALENV="venv"

if [ -e "$VIRTUALENV/bin/activate" ]; then
  source "$VIRTUALENV/bin/activate"
elif [ -e "$VIRTUALENV/Scripts/activate" ]; then
  source "$VIRTUALENV/Scripts/activate"
else
  echo "Could not find virual environment '$VIRTUALENV'"
fi
