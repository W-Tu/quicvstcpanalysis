#!/bin/sh

while true
do
	python3 ../../aioquic/examples/http3_client.py --zero-rtt -k $1 &
	sleep $2;
done
