import numpy as np
import pandas as pd
from pathlib import Path


def summarize(df_: pd.DataFrame, outdir: Path) -> None:
    """Summarize the data and save results"""


    if not outdir.exists():
        outdir.mkdir(parents=True)

    df = df_.copy()

    # Number of epochs per filter per obect
    summary_object = pd.pivot_table(
        df,
        values="mag",
        index="source_id",
        columns="filter",
        aggfunc=["count", "median"],
    )
    summary_object.to_csv(outdir / "summary_by_object.csv")

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
    summary_rrlyrae_type.to_csv(outdir / "summary_by_rrlyrae_type.csv")
