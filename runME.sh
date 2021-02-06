#!bin/bash
if [[ -f "./Data" ]]
then
    bash -c './sysFiles/main.py'
else
    bash -c './sysFiles/setup.py'
fi