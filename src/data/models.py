from dataclasses import dataclass, field
from enum import Enum

from astropy.coordinates import SkyCoord
from astropy.table import Table

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
    date: str
    filter: NIRFilter
    coords: SkyCoord  = field(repr=False)

    def __post_init__(self) -> None:
        """Post init method"""
        self.table["date"] = self.date
        self.table["filter"] = self.filter.value


@dataclass
class RRLyrae:
    """Class used to store RRLyrae stars from Ramos et al. 2020"""
    table: Table

    @property
    def coords(self) -> SkyCoord:
        return SkyCoord(self.table["RA_ICRS"], self.table["DE_ICRS"])

