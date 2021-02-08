#!/bin/bash
if [[ -f "./Data/.setupComp" ]]
then
        cd "$(dirname "$0")"; python ./sysFiles/main.py
else
        cd "$(dirname "$0")"; python ./sysFiles/setup.py
fi
