from src.data.models import Catalog, NIRFilter, RRLyrae
from astropy.table import Table, hstack, vstack

TOLERANCE: float = 0.34


def gather_data(rrlyrae: RRLyrae, catalogs: list[Catalog]) -> Table:
    """Extract corresponding data from catalogs for all sources in rrlyrae"""
    
    output_table = Table()
    for catalog in catalogs:

        t = match_catalogs(rrlyrae, catalog)
        output_table = vstack([output_table, t])

    return output_table


def match_catalogs(rrlyrae: RRLyrae, catalog: Catalog) -> Table:
    """Match catalogs using coordinates and return a table with the matches"""

    idx, d2d, _ = rrlyrae.coords.match_to_catalog_sky(catalog.coords)
    mask = d2d.arcsec < TOLERANCE

    return hstack([rrlyrae.table, catalog.table[idx]])[mask]
