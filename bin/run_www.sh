#!/usr/bin/env bash

for i in $(seq 0 9); do
    year=y${i}
    cd $year
    python ../bin/www.py 
    cd -
done
