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
    obsdates = {}
    filters = {}
    with open(dir_path / LOGFILE) as file:
        for line in file:
            (key, dateobs, filter) = line.replace("'", "").split()
            obsdates[key] = dateobs
            filters[key] = filter

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

        print("Processing", str(table_file.stem))  # TODO: remove

        # Read data for every file
        table = Table.read(table_file, format="ascii", names=colnames)
        name = table_file.stem

        # Read coordinates and update table
        coords = get_coordinates(table)
        table["ra"] = coords.ra
        table["dec"] = coords.dec

        catalog = Catalog(
            name=name,
            table=table,
            # date=obsdates[name],
            date=Time(obsdates[name], format='isot', scale='utc'),
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
