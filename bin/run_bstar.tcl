#!/usr/bin/tclsh

# Run the bstarJob for a single year.

# The year variable can be set explicitly:
#set year 0
# Or passed in (see run.sh):
#echo "set year 0; source run.tcl" | ./ktools

if {![info exists year]} {
    puts "${year} does indeed exist; exiting..."
    exit
}

puts "Running bstar..."
set filename "./survey-y${year}.txt"
puts $filename
puts "  Read $filename"
surveyRead $filename
puts "  Run bstarJob..."
bstarJob
puts "  Set header"
keylset hdr comment "Year ${year} bright stars"
puts "  Write survey-y${year}.par"
chain2Param "survey-y${year}.par" h0 $hdr

puts "Done."
exit
