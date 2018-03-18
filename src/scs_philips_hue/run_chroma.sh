#!/usr/bin/env bash

# $1: optional -v

./osio_mqtt_subscriber.py $1 -c | ./node.py $1 -c | ./chroma.py $1 | ./desk.py $1 -e
