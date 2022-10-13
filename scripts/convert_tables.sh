#!/bin/bash

# Convert fits tables to ascii file. Observation date is saved to a log file.
# Reference regex lookahead: https://stackoverflow.com/questions/1454913/regular-expression-to-find-a-string-included-between-two-characters-while-exclud

OUTPUT_FILE="catalogue.asc"
INPUT_DIR="raw_fits_tables"
OUTPUT_DIR="ascii_tables_no-tiled"
LOG_FILE="log.txt"
GETDATEOBS() { fitsheader -k DATE-OBS $1 | grep -Eho "'.*'" | head -n 1; };
GETMJDOBS() { fitsheader -k MJD-OBS $1 | grep -Pho "(?<==).*(?=\s/)" | head -n 1; };
GETFILTER() { fitsheader -k "HIERARCH ESO INS FILT1 NAME" $1 | grep -Eho "'.*'" | head -n 1; };


rm -rf $OUTPUT_DIR
mkdir -p $OUTPUT_DIR

for file in $INPUT_DIR/*_st_cat.fits;
do
    echo "Processing $file"

    # Extract observation date from header and save it to a log file
    dateobs=$(GETDATEOBS $file)
    filter=$(GETFILTER $file)
    mjd=$(GETMJDOBS $file)
    filestem=$(basename $file .fits)
    echo "$filestem $dateobs $filter '$mjd'" >> $OUTPUT_DIR/$LOG_FILE
    
    # Process the .fits table
    fitsio_cat_list $file
    mv -- $OUTPUT_FILE $OUTPUT_DIR/$filestem.asc
done;
