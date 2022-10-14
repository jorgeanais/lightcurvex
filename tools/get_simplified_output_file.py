#! /usr/bin/python
import pandas as pd

"""
Script used to get the simplified output file from the original output file.
Used to share the results with the collaborators.
"""

FILENAME = "6760320515827605760"
df = pd.read_csv(f"{FILENAME}.csv")

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
        f"{FILENAME}_{filt}.csv", index=False
    )
