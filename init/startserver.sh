#! /bin/bash
while true; do
    avconv -fpsprobesize 0 -analyzeduration 0 -re -i /shared/test.h264 -c copy -f h264 udp://239.0.1.23:1234
done
