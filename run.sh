#!/bin/bash

for fp in $(seq 0 10 500)
do
	echo "VAR = $fp"
	python test.py effect_of_Pcc $fp
done
