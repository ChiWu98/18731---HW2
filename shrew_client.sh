#!/bin/bash 

echo running iperf-client

#TODO: add your code


for i in {1..100}
do
    iperf -c 10.0.0.1 -p 5006  -t 0.15 -u -b 10M &
    #iperf -c 10.0.0.1 -u -b 10M -p 5006 -t 0.25
    sleep 0.85
done
