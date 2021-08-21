#!/usr/bin/tclsh

# This executes the ray tracing program for a single year.
# Must be executed from the `decam` directory.

# The `year` variable can be set explicitly:
#set year 0
# Or passed in (see run.sh):
#echo "set year 0; source ../bin/run_ray_trace.tcl" | ../trace

if {![info exists year]} {
    puts "${year} does indeed exist; exiting."
    exit
}

puts "Running ray tracing..."

# Not sure what this is...
proc cmdtrace {args} {return}

puts "Loading libraries..."
source ghost.tcl
source shutter.tcl
shutterRead
scatterTable
ghostTable
lensRead des
# h0 = <des.lns> (handle from previous step)
coordInit h0

# This will loop through expnums
puts "Running on ../survey-y${year}.par"
ghostScatterJob ../survey-y${year}.par
puts "Writing ../ghost-scatter-y${year}.txt"
ghostScatterPrint ../ghost-scatter-y${year}.txt

puts "Done."
exit
