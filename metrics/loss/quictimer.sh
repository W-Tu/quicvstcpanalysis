#!/bin/bash

end=50

for ((j=0; j<=100; j+=10)) do
	read -p "Press any key to continue to log $j"
	for ((i=0; i<$end; i++))  do
		((time python3 examples/http3_client.py --zero-rtt -k https://192.168.100.52:443) 2>&1 | grep ^real >> logs/$1/quic/$j.log) &
		echo "$i / $end"
		sleep 1
	done
done
