#!/usr/bin/env bash

#for i in 0; do
for i in $(seq -w 0 11); do
    year=y${i}
    echo $year
    cd $year
    python ../bin/www.py 
    cd -
done
