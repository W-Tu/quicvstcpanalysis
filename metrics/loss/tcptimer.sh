#!/bin/bash

end=50

for ((j=0; j<=100; j+=10)) do
	read -p "Press any key to continue to log $j"
	for ((i=0; i<$end; i++))  do
		((time curl -k https://192.168.100.52:80) 2>&1 | grep ^real >> logs/$1/tcp/$j.log) &
		echo "$i / $end"
		sleep 1
	done
done
