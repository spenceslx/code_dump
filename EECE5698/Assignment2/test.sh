#!/bin/bash
#script to test for loop

ARRAY=( 1 2 4 8 16 32 64 )
#number of elements in array
ELEMENTS=${#ARRAY[@]} 

for ((i=0;i<$ELEMENTS;i++)); do
	echo ${ARRAY[${i}]}
done


