#!/bin/bash

for eff in $(seq 50 10 100)
do
	echo "eff = $eff"
	for fp in $(seq 2 0.1 10)
	do
		echo "VAR = $fp"
		python test.py effect_of_burntime $fp $eff
	done
done
