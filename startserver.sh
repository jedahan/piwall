#! /bin/bash
sleep 15
avconv -re -i /shared/test.avi -vcodec copy -an -f avi udp://239.0.1.23:1234
