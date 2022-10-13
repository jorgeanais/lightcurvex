from pathlib import Path
from typing import Any

from astropy.coordinates import SkyCoord
from astropy.table import Table
from astropy.time import Time

from .models import Catalog, NIRFilter, RRLyrae


LOGFILE = "log.txt"


def concatenate_columns(
    columns: list[str], table: Table, delimiter: str = ":"
) -> list[str]:
    """Concatenate columns of a table"""

    aux = []
    for column in columns:
        data = list(table[column].data.astype(str))
        aux.append(data)

    return [delimiter.join(x) for x in zip(*aux)]


def get_coordinates(
    table: Table,
    ra_cols: tuple[str, str, str] = ("ra_h", "ra_m", "ra_s"),
    dec_cols: tuple[str, str, str] = ("dec_d", "dec_m", "dec_s"),
) -> SkyCoord:
    """Parse coordinates from multiple columns"""

    ra = concatenate_columns(ra_cols, table)
    dec = concatenate_columns(dec_cols, table)
    return SkyCoord(ra, dec, unit=("hourangle", "deg"))


def load_catalogs(dir_path: Path) -> list[Catalog]:
    """Load all CASU VVVX ascii catalogs from path"""

    # Load header keys from log file
    obsdates = {}
    filters = {}
    obsmjds = {}
    with open(dir_path / LOGFILE) as file:
        for line in file:
            (key, dateobs, band, obsmjd) = line.replace("'", "").split()
            obsdates[key] = dateobs
            filters[key] = band
            obsmjds[key] = float(obsmjd)

    # Read and create catalogs
    catalogs = []
    colnames = (
        "ra_h",
        "ra_m",
        "ra_s",
        "dec_d",
        "dec_m",
        "dec_s",
        "x",
        "y",
        "mag",
        "mag_error",
        "chip_number",
        "stellar_class",
        "ellipticity",
        "position_angle",
    )

    for table_file in dir_path.glob("*.asc"):

        name = table_file.stem
        print("Processing", str(name))

        # Try read data for every file, otherwise skip it 
        # Problem with one file (v20180524_01557_st_cat), on one line (52385). 
        # Simple solution is just remove that line
        try:
            table = Table.read(table_file, format="ascii", names=colnames)
        except Exception as e:
            print("Error reading file", table_file.stem, e)
            print()
            continue

        # Read coordinates and update table with ra and dec in degrees
        coords = get_coordinates(table)
        table["ra"] = coords.ra
        table["dec"] = coords.dec

        # Create and object to wrap the table and to include metadata
        catalog = Catalog(
            name=name,
            table=table,
            obsmjd=obsmjds[name],
            date=Time(obsdates[name], format="isot", scale="utc"),
            filter=NIRFilter(filters[name]),
            coords=coords,
        )
        catalogs.append(catalog)

    return catalogs


def load_RRLyrae(path: Path) -> RRLyrae:
    """
    Load RRLyrae catalog from path
    Sources from Ramos et al. 2020 within tile 0411
    """
    table = Table.read(path, format="votable")
    rrlyrae = RRLyrae(table=table)
    return rrlyrae
