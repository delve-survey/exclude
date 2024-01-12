# DECam Exclude Lists

Assemble lists of bad/suspect DECam data to exclude from high-level processing. These lists are collected using a number of techniques, including visual inspection. These lists follow the same format as the DES exclusion lists found [here](https://des-ops.fnal.gov:8082/exclude/).

## Execution

Create pngs of the problem exposures:
```bash
./bin/run_png.sh
```
Assemble the webpages:
```bash
./bin/run_www.sh
```
Compile the list of excluded CCD images (expnum/ccdnum) where `YYYYMMDD` is the current date:
```bash
python bin/make_exclude_list.py y*/*.txt -o delve_exclude_YYYYMMDD.fits
```

Upload list to the DESDM Oracle database:
```bash
easyaccess -s decade -lt delve_exclude_YYYYMMDD.fits
easyaccess -s decade -c "grant select on DELVE_EXCLUDE_YYYYMMDD to PUBLIC;"
```
