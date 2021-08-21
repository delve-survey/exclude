#!/usr/bin/env bash

# This loop is outside of tcl because variables are not being unset in
# the way I'd expect...
for year in $(seq 0 9); do
    echo "set year ${year}; source run_bstar.tcl" | ./ktools
done
