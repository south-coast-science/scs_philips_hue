#!/usr/bin/env bash

# $1: topic path
# $2: document node
# $3: domain max
# $4: brightness
# $5: lamp name
# $6: optional -v

# example: ./run_chroma.sh /orgs/south-coast-science-demo/brighton/loc/1/particulates val.pm2p5 50 128 scs-hcl-001 &

./osio_mqtt_subscriber.py $6 $1 | ./node.py $5 $1.$2 | ./chroma.py $6 -d 0 $3 -r G R -t 9.0 -b $4 | ./desk.py $6 $5
