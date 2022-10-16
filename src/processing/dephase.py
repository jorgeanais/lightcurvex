import numpy as np
import pandas as pd

from astropy.table import Table, vstack


def get_period(
    df: pd.DataFrame,
    period_cols: list[str] = ["pf", "p1_o"]
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


def process_phase_folding(table: Table, id_col: str = "source_id") -> Table:
    """
    Phase folding for all sources.
    """

    df = table.to_pandas()
    # df.drop(columns=["priam_flags"], inplace=True)  # TODO: remove this line
    output_table = Table()

    # Process one object at a time
    ids = list(df[id_col].unique())
    list_of_tables = []
    for id in ids:
        print("dephasing: ", id)
        single_object_df = df.query(f"{id_col} == {id}").copy()

        # Add a column with the phase
        single_object_df["period"] = get_period(single_object_df)
        single_object_df["phase"] = phase_folding(single_object_df)
        single_object_table = Table.from_pandas(single_object_df)
        
        list_of_tables.append(single_object_table)

    
    output_table = vstack(list_of_tables, "inner")
            


    return output_table