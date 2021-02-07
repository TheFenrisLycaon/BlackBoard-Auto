#!bin/bash
if [[ -f "./Data/.setupComp" ]]
then
        python ./sysFiles/main.py
else
        python ./sysFiles/setup.py
fi
