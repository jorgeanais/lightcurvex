#! /usr/bin/python
"""
Save ascii catalogs to votable format after coords processing
"""
import sys

sys.path.append("../")

from pathlib import Path

from src.data.loader import load_catalogs


DATA_DIR = Path("/home/jorge/Documents/data/CASU_411/tables/ascii_tables_no-tiled/")
OUTPUT_DIR = Path(
    "/home/jorge/Documents/data/CASU_411/tables/ascii_tables_no-tiled/votable/"
)

# Time consuming part
catalogs = load_catalogs(DATA_DIR)

# Save catalogs in VOT format
if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir(parents=True)

for catalog in catalogs:
    catalog.table.write(str(OUTPUT_DIR / f"{catalog.name}.vot"), format="votable")
