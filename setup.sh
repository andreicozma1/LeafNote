#!/bin/sh

show_install() {
  echo " # To proceed, please install Python3 and Pip3." &&
    echo " # Linux: sudo apt-get install python3 python3-pip" &&
    echo " # macOS: brew install python3 python3-pip" &&
    echo " # Windows: https://www.python.org/downloads"
}

if which python3 >/dev/null 2>&1; then
  echo "## Checking Python Version:" &&
    python3 -V &&
    if which pip3 >/dev/null 2>&1; then
      echo "" &&
        echo "## Checking Pip3 Version:" &&
        pip3 -V &&
        if (pip3 show virtualenv | grep -i version) >/dev/null 2>&1; then
          echo "" &&
            echo "## Creating Virtual Environment:"
        else
          pip3 install virtualenv
        fi

      python3 -m virtualenv .venv &&
        echo "" &&
        echo "## Activating Virtual Environment:" &&
        source .venv/bin/activate &&
        echo "" &&
        echo "## Installing Project Dependencies:" &&
        pip3 install -r requirements.txt &&
        echo "" &&
        echo "## All done!"
      echo " # Use the run script to execute the program!"
    else
      echo "## ERROR: Pip3 is not installed on your system!" &&
        show_install
    fi
else
  echo "## ERROR: Python3 is not installed on your system!" &&
    show_install
fi
