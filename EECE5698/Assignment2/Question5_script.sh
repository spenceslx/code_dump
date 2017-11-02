#!/bin/bash
#script to run results from question 5, in order appearing in MSE.o

COUNT=0

rm TIME.o
rm MSE.o

#iterate while count less than 21 (up to 20)
while [ $COUNT -lt 21 ]; do
	echo $COUNT
	spark-submit --master local[40] --driver-memory 100G ParallelRegression.py \
		           --train data/big.train   --test data/big.test  \
		           --beta beta_big_0.0 	--lam $COUNT  --silent
	let COUNT=COUNT+1
	sleep 30
done
