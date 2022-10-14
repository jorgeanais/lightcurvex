#! /usr/bin/python
"""
Condense all the csv files into a single table with one row per object
"""
import pandas as pd
from pathlib import Path


INPUT_DIR = Path(
    "/home/jorge/Documents/data/CASU_411/tables/ascii_tables_no-tiled/output_dephase/"
)

fixed_columns = [
    "GaiaDR2",
    "Gmag",
    "RA_ICRS",
    "DE_ICRS",
    "pmRA",
    "pmDE",
    "SOStype",
    "VCtype",
    "PS1type",
    "period",
]
cols_to_group = ["filter", "mag"]

rows = []

for file in INPUT_DIR.glob("*.csv"):
    print(file)
    df = pd.read_csv(file)
    sfix = df[fixed_columns].iloc[0]
    smean = df[cols_to_group].groupby("filter").mean().T.iloc[0]

    row = pd.concat([sfix, smean], axis=0)
    rows.append(row)


df = pd.DataFrame(rows)
print(df)
df.to_csv("agg_values_RRLyrae.csv", index=False)
