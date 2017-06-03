#!/bin/bash
# Works for Jabra SPEAK 410 USB running on Raspberry Pi 3

for i in $(seq -f "%02g" 01 99)
do
    new_file="sounds/shush_$i.wav"
    [ ! -f "$new_file" ] && break
done

arecord -f S16_LE -r 48000 -D plughw:1,0 -d 1 "$new_file"
