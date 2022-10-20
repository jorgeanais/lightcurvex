from dataclasses import dataclass, field
from enum import Enum

from astropy.coordinates import SkyCoord
from astropy.table import Table
from astropy.time import Time


# Ra and dec columns of the RRLyrae reference catalog
RA_RRL_COL = "RAJ2000"
DEC_RRL_COL = "DEJ2000"


class NIRFilter(Enum):
    """List possible NIR bands"""

    J = "J"
    H = "H"
    Ks = "Ks"


@dataclass
class Catalog:
    """Class used to store information related with CASU ascii catalogs"""

    name: str
    table: Table = field(repr=False)
    date: Time
    obsmjd: float
    filter: NIRFilter
    coords: SkyCoord = field(repr=False)

    def __post_init__(self) -> None:
        """Post init method"""
        self.table["date"] = self.date.isot
        self.table["mjd"] = self.date.mjd
        self.table["filter"] = self.filter.value
        self.table["obsmjd"] = self.obsmjd


@dataclass
class RRLyrae:
    """Class used to store RRLyrae stars from Ramos et al. 2020"""

    table: Table

    @property
    def coords(self) -> SkyCoord:
        return SkyCoord(self.table[RA_RRL_COL], self.table[DEC_RRL_COL])