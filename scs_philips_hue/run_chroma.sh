#!/usr/bin/env bash

# $1: topic path
# $2: document node
# $3: brightness
# $4: lamp name
# $5: optional -v

# example: ./run_chroma.sh /orgs/south-coast-science-demo/brighton/loc/1/particulates val.pm2p5 128 scs-hcl-001 &

./osio_mqtt_subscriber.py $5 $1 | ./node.py $5 $1.$2 | ./chroma.py $5 -d 0 50 -r G R -t 9.0 -b $3 | ./desk.py $5 $4
