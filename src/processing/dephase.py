import numpy as np
import pandas as pd

from astropy.table import Table, vstack


# Column name used to group objects (RR Lyrae catalog)
SOURCE_ID = "Star" #  "source_id"
PERIOD_COLS = ["Per"]#  ["pf", "p1_o"]

def get_period(
    df: pd.DataFrame,
    period_cols: list[str] = PERIOD_COLS
) -> np.ndarray:
    """
    Get the period from the input dataframe for a single object.

    `period_cols` indicate the names of the columns that contain information about the period.
        Depending on the type of the RR Lyrae, it could include overtones or not.
        Period is assumed in units of days. Its value is obtained from the RR Lyrae catalog.
    """

    df = df.copy()
    
    return df[period_cols].mean(axis=1).values


def phase_folding(
    df: pd.DataFrame, 
    period_col: str = "period",
    date_col: str = "obsmjd"
) -> np.ndarray:
    """
    Phase folding for a single source.

    `period_col` indicates the name of the column that contains information about the period. It is expected that this
        column has the same value repeated, because it is the same source.
    
    `date_col` is the column with the date of observation in days. It can be "mjd" (obtained from DATE-OBS header keyword)
        or "obsmjd" (obtained from MJD-OBS header keyword).
    """

    df = df.copy()
    date_origin = df[date_col].min()
    

    # Phase folding
    df["phase"] = (df[date_col] - date_origin) % df[period_col] / df[period_col]

    return df["phase"].values


def shift_phase(
    df: pd.DataFrame,
    shift: float = 0.5,
    phase_col: str = "phase",
) -> np.ndarray:
    """
    Shift the phase by a given amount.
    """

    df = df.copy()
    df[phase_col] = df[phase_col] - shift

    return df[phase_col].values


def find_minimum_phase(
    df: pd.DataFrame,
    phase_col: str = "phase",
    mag_col: str = "mag",
    filter_col: str = "filter",
    band: str = "Ks",
) -> float:
    """
    Find the phase of the minimum magnitude.
    """

    df = df.copy()
    df.query(f"{filter_col} == '@band'", inplace=True)
    min_phase = df.loc[df[mag_col].idxmin()][phase_col]

    return min_phase


def process_phase_folding(table: Table, id_col: str = SOURCE_ID) -> Table:
    """
    Phase folding for all sources.
    """

    df = table.to_pandas()
    output_table = Table()

    # Process one object at a time
    ids = list(df[id_col].unique())
    list_of_tables = []
    for id in ids:
        print("dephasing: ", id)
        single_object_df = df.query(f"{id_col} == '{id}'").copy()

        # Add a column with the phase
        single_object_df["period"] = get_period(single_object_df)
        single_object_df["phase"] = phase_folding(single_object_df)
        
        # Shift phase so start at minimum
        min_phase = find_minimum_phase(single_object_df)
        single_object_df["phase"] = shift_phase(single_object_df, shift=min_phase)
        
        single_object_table = Table.from_pandas(single_object_df)
        
        list_of_tables.append(single_object_table)

    
    output_table = vstack(list_of_tables, "inner")
            


    return output_table