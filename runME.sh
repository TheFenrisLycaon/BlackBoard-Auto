#!/bin/bash
if [[ -f "./Data/.setupComp" ]]
then
        cd "$(dirname "$0")"; bash ./src/tt.sh
else
        cd "$(dirname "$0")"; python ./src/setup.py
fi
