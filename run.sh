#!/bin/bash

for var1 in $(seq 4 1 4)
do
	echo "OF = $var1"
	for var2 in $(seq 4 0.5 12)
	do
		echo "burntime = $var2"
		python test.py effect_of_burntime $var2
	done
done
