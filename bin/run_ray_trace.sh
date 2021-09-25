#!/usr/bin/env bash

cd decam

# This loop is outside of tcl because variables are not being unset in
# the way I'd expect...
for year in $(seq 0 9); do
    echo "set year ${year}; source ../bin/run_ray_trace.tcl" | ../trace
done

cd -
