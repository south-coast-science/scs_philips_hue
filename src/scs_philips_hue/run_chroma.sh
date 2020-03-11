#!/usr/bin/env bash

# $1: optional -v

# ./aws_mqtt_subscriber.py -v -c | ./node.py -v -c | ./chroma.py -v | ./desk.py -v

./aws_mqtt_subscriber.py $1 -e -c | ./node.py $1 -c | ./chroma.py $1 | ./desk.py $1
