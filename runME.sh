#!/bin/bash
if [[ -f "./Data/.setupComp" ]]
then
        cd "$(dirname "$0")"; bash ./sysFiles/tt.sh
else
        cd "$(dirname "$0")"; python ./sysFiles/setup.py
fi
