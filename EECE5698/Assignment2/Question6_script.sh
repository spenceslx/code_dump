#!/bin/bash
#script to run results from question 6, in order appearing in TIME.o

N=( 1 2 4 8 16 32 64)
#number of elements in array
ELEMENTS=${#N[@]}

rm TIME.o
rm MSE.o

for ((i=0;i<$ELEMENTS;i++)); do
	ulimit -u 10000
	echo N = ${N[${i}]}
	spark-submit --master local[${N[${i}]}] --driver-memory 100G ParallelRegression.py \
		           --train data/very_big.train   --test data/very_big.test  \
	        	   --beta beta_very_big_0.0 	--lam 10.0  --silent
	sleep 30
done
