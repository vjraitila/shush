#!/bin/bash

for i in $(seq -f "%02g" 01 99)
do
    new_file="sounds/shush_$i.wav"
    if [ ! -f "$new_file" ]; then break; fi
done

arecord -f S16_LE -r 48000 -D plughw:1,0 -d 1 "$new_file"
