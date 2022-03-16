#!/bin/bash 

echo running iperf-client

#TODO: add your code
<<<<<<< HEAD
<<<<<<< HEAD


=======
>>>>>>> e411c8c16118d7412a41befe5bb4416576d721c6
for i in {1..200}
do
    iperf -c 10.0.0.1 -p 5006  -t 0.1 -u -b 10M &
    #iperf -c 10.0.0.1 -u -b 10M -p 5006 -t 0.25
    sleep 0.9
done
<<<<<<< HEAD
=======
>>>>>>> 08c7f51ba12a7711d270171692984835361a305f
=======
>>>>>>> e411c8c16118d7412a41befe5bb4416576d721c6
