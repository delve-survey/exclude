# Exclude

Assemble lists of bad data to exclude from processing.

## Execution

Create pngs:

./bin/run_png.sh

Assemble webpages:

./bin/run_www.sh

Compile the final list of excluded CCDs:

python bin/make_exclude.py y*/*.txt -o delve_exclude_YYYYMMDD.fits

Upload list to desdm

easyaccess -s decade -lt delve_exclude_YYYYMMDD.fits