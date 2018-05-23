#!/bin/bash

rm -rf nohup.out
#rm -rf data/*

#nohup python3 DaumNewsCrawler.py -i 0.5 -d 20180501 &
#python3 DaumNewsCrawler.py -i 0.1 -d 20180501
python3 news_crawler.py -i 0.1 -d 20180501
