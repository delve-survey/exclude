#!/usr/bin/env bash

#urls=delve-urls-v1.csv 
#urls=delve-urls-v2.csv
#urls=decade-urls-qa.csv
#urls=decade-urls-qa-v2.csv
#urls=decade-urls-v3.csv
urls=decade-urls-qa-v4.csv
paths=delve-paths-v0.csv

#for i in $(seq 0 9); do
for i in 09; do
    year=y${i}
    filename=${year}/ghost-scatter-${year}.txt
    log=${year}/run_pngs.log
    #csub -o $log python ./bin/pngs.py $filename $urls -p $paths -o ${year}/pngs
    python ./bin/pngs.py $filename $urls -p $paths -o ${year}/pngs
done
