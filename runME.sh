#!bin/bash
if [[ -d "./Data" ]]
then
        python ./sysFiles/main.py
else
        python ./sysFiles/setup.py
fi
