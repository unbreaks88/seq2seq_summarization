#!/bin/bash

start_date=$1
end_date=$2
log=${start_date}.log

echo $log

if [ -z $start_date ] && [ -z $end_date ]; then
	echo "Start_date, end_date must be needed"
	exit -1
fi

nohup python3 news_crawler.py -i 0.01 -s $start_date -e $end_date > $log 2>&1
