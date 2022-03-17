#qsize=$1
echo set iperf-server

#TODO: add your code

iperf -s -u -p 5006 -t 500 &
