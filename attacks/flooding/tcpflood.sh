#!/bin/sh

while true
do
	curl -k $1 &
	sleep $2;
done
