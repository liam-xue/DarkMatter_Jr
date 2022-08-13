#!/bin/bash

for eff in $(seq 90 10 90)
do
	echo "eff = $eff"
	for bt in $(seq 2 1 10)
	do
		echo "burntime = $bt"
		python test.py effect_of_burntime $bt $eff
	done
done
