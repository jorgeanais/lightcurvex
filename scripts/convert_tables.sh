#!/bin/bash

# Extract fits tables to ascii file. Observation date is saved to a log file.

OUTPUT_FILE="catalogue.asc"
OUTPUT_DIR="ascii_tables"
LOG_FILE="obsdates.txt"
GETDATEOBS() { fitsheader -k DATE-OBS $1 | grep -Eho "'.*'" | head -n 1; };

rm -rf $OUTPUT_DIR
mkdir -p $OUTPUT_DIR

for file in *_tl_cat.fits;
do
    echo "Processing $file"

    # Extract observation date from header and save it to a log file
    dateobs=$(GETDATEOBS $file)
    echo "$file $dateobs" >> $OUTPUT_DIR/$LOG_FILE
    
    # Process the .fits table
    fitsio_cat_list $file
    mv -- $OUTPUT_FILE $OUTPUT_DIR/${file%.fits}.asc
done;