from warnings import filterwarnings
import numpy as np
import pandas as pd
from pathlib import Path


def summarize(df_: pd.DataFrame, outdir: Path) -> None:
    """Summarize the data and save results"""

    df = df_.copy()

    n_objects = len(df["GaiaDR2"].unique())
    filters = df["filter"].unique

    # Number of epochs per filter per obect
    summary_object = pd.pivot_table(
        df,
        values="recno",
        index="GaiaDR2",
        columns="filter",
        aggfunc=["count", "median"],
    )
    summary_object.write(outdir / "summary_by_object.csv", overwrite=True, format="csv")

    # Summary of Types of RR Lyrae
    for col in ["VCtype", "PS1type", "SOStype"]:
        df[col] = df[col].fillna("-")

    summary_rrlyrae_type = pd.pivot_table(
        df,
        values=["mag"],
        index=["VCtype", "PS1type", "SOStype"],
        columns="filter",
        aggfunc=["count", "mean", "std"],
        fill_value="-",
    )
    summary_rrlyrae_type.write(
        outdir / "summary_by_rrlyrae_type.csv", overwrite=True, format="csv"
    )
