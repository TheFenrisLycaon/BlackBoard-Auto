#!/bin/bash

t=$(date +%H%M)
d=$( expr $(date +%u) - 1 )

if [ $t -le 999 ]
then
    echo "Waiting for $( expr 999 - $t - 40) minutes"
    sleep $( expr 999 - $t - 40)m
    t=$(date +%H%M)
elif [ $t -ge 1630 ]
then
    echo "You're too late to handle the power of spinzitzu";exit
else
    echo "Getting in class"
fi

while [ $t -lt 1630 ]
do
    if [ $t -le 1044 -a $t -ge 959 ]
    then
        l=1
        t=$(date +%H%M)
        limit=$(expr 1100 - $t - 40)
    elif [ $t -le 1144 -a $t -ge 1059 ]
    then 
        l=2
        t=$(date +%H%M)
        limit=$(expr 1200 - $t - 40)
    elif [ $t -le 1244 -a $t -ge 1159 ]
    then 
        l=3
        t=$(date +%H%M)
        limit=$( expr 1345 - $t - 40)
    elif [ $t -le 1344 -a $t -ge 1244 ]
    then 
        l=4
        t=$(date +%H%M)
        limit=$( expr 1345 - $t - 40)
    elif [ $t -le 1430 -a $t -ge 1344 ]
    then 
        l=5
        t=$(date +%H%M)
        limit=$( expr 1445 - $t - 40)
    elif [ $t -le 1530 -a $t -ge 1444 ]
    then 
        l=6
        t=$(date +%H%M)
        limit=$( expr 1545 - $t )
    elif [ $t -le 1630 -a $t -ge 1544 ]
    then 
        l=7
        t=$(date +%H%M)
        limit=$( expr 1630 - $t - 40)
    else
        echo "You're too late to handle the power of spinzitzu";exit
    fi

    c=$(( $d *10 + $l + 1))
    #echo $c
    #for entry in `ls ./`; do
        #echo $entry
    #done
    calpath='./Data/.calFile'
    link=$(sed -n "${c}p" "$calpath")
    echo $link
    brave $link --noerrdialogs
    echo "Waiting for $limit minutes"
    sleep "$limit"m
    t=$(date +%H%M)
done
