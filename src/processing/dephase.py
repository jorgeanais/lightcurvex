import numpy as np
import pandas as pd


def phase_folding(df: pd.DataFrame, period_cols: list[str] = ["pf", "p1_o"], date_col: str = "mjd") -> np.ndarray:
    """
    Phase folding for a single source.
    
    Period is assumed in units of days, and date_col is assumed to be in MJD.
    
    Reference
    https://docs.astropy.org/en/stable/timeseries/lombscargle.html
    """
    
    df = df.copy()
    date_origin = df[date_col].min()
    
    df["period"] = df[period_cols].mean(axis=1).values

    # Phase folding
    df["phase"] = (df[date_col] - date_origin) % df["period"] / df["period"]

    return df["phase"].values