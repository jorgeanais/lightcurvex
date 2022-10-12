import numpy as np
import pandas as pd
from pathlib import Path

from astropy.table import Table
import matplotlib.pyplot as plt
from scipy.stats import median_absolute_deviation

from .dephase import phase_folding


def plot_data(
    table: Table, output_dir: Path, id_col: str = "GaiaDR2", filter_col: str = "filter"
) -> None:
    """
    Generate plots for all the objects in the table (i.e. VVV sources that match the RR Lyrae stars).
    One plot per object and filter combination.
    """

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    df = table.to_pandas()
    ids = list(df[id_col].unique())

    # Save objects independently
    for id in ids:

        single_object_df = df.query(f"{id_col} == {id}").copy()

        # Add a column with the phase
        single_object_df["phase"] = phase_folding(single_object_df)

        filters = list(single_object_df[filter_col].unique())

        for f in filters:
            single_filter_object_df = single_object_df.query(
                f"{filter_col} == '{f}'"
            ).copy()
            plot_variable_star(single_filter_object_df, output_dir)


def plot_variable_star(
    df: pd.DataFrame,
    output_dir: Path,
    x_col: str = "phase",
    y_col: str = "mag",
    y_err_col: str = "mag_error",
    filter_col: str = "filter",
    vtype_col: str = "SOStype",
) -> None:
    """Plot a single variable star light curve"""

    # Prepare data
    if y_col == "date":
        df[x_col] = pd.to_datetime(df[x_col])

    object = df["GaiaDR2"].unique()[0]
    filter = df[filter_col].unique()[0]
    vtype = df[vtype_col].unique()[0]
    median_mag = df[y_col].median()
    mad = median_absolute_deviation(df[y_col].values)

    plt.figure(figsize=(10, 8))
    plt.errorbar(df[x_col], df[y_col], yerr=df[y_err_col], fmt="o")
    plt.plot(df[x_col], df[y_col], "o")
    plt.xlabel(f"{x_col}")
    plt.ylabel(f"{y_col}")
    plt.title(f"{object=} {filter=} {vtype=} {median_mag=:.3f} {mad=:.3f}")

    plt.savefig(output_dir / f"{object}_{filter}_{vtype}.png")
    plt.clf()
    plt.close()
