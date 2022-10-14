#! /usr/bin/python
import pandas as pd
from pathlib import Path

"""
Script used to get the simplified output file from the original output file.
Used to share the results with the collaborators.
"""

INPUT_FILE = Path("/home/jorge/Documents/data/CASU_411/tables/ascii_tables_no-tiled/output_dephase/6760320515827605760.csv")
OUTPUT_DIR = Path("/home/jorge/")

df = pd.read_csv(INPUT_FILE)

columns_of_interest = [
    "GaiaDR2",
    "RA_ICRS",
    "DE_ICRS",
    "GLON",
    "GLAT",
    "SOStype",
    "PS1type",
    "VCtype",
    "best_classification",
    "pf",
    "pf_error",
    "ra",
    "dec",
    "date",
    "mjd",
    "filter",
    "mag",
    "mag_error",
    "chip_number",
    "stellar_class",
    "ellipticity",
    "position_angle",
]

for filt in list(df["filter"].unique()):
    print(filt)
    df.query("filter == @filt")[columns_of_interest].to_csv(
        OUTPUT_DIR / f"{INPUT_FILE.stem}_{filt}.csv", index=False
    )
