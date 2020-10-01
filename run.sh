#!/bin/bash
FILE=.venv/bin/activate
if [ -f "$FILE" ]; then
  echo "## Activating Virtual Environment:" &&
    source "$FILE"
  echo "" &&
    echo "## Starting Application:" &&
    fbs clean && fbs run
else
  echo "## ERROR: Python Virtual Environment missing!"
  echo " # Please run the setup script first!"
fi
