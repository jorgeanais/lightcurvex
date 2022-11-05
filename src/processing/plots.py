import numpy as np
import pandas as pd
from pathlib import Path

from astropy.table import Table
import matplotlib.pyplot as plt
from scipy.stats import median_abs_deviation


# Column used to group objects
SOURCE_ID = "Star"
VTYPE_COL = "Type"


def plot_data(
    table: Table, output_dir: Path, id_col: str = SOURCE_ID, filter_col: str = "filter"
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

        single_object_df = df.query(f"{id_col} == '{id}'").copy()

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
    vtype_col: str = VTYPE_COL,
    id_col: str = SOURCE_ID,
    period_col: str = "period",
    double_phase: bool = True,
) -> None:
    """Plot a single variable star light curve"""

    # Prepare data
    if y_col == "date":
        df[x_col] = pd.to_datetime(df[x_col])

    object = df[id_col].unique()[0]
    filter = df[filter_col].unique()[0]
    vtype = df[vtype_col].unique()[0]
    median_mag = df[y_col].median()
    mad = median_abs_deviation(df[y_col].values)
    period = df[period_col].unique()[0]

    plt.figure(figsize=(10, 8))

    # Plot data (repeat the phase if `double_phase` is True)
    for phase in range(double_phase + 1):
        x = df[x_col] + phase
        y = df[y_col]
        yerr = df[y_err_col]
        plt.errorbar(x, y, yerr=yerr, fmt="o", c="gray", alpha=0.2, )
        plt.plot(x, y, "o", c="black")
    
    ymin, ymax = plt.ylim()
    plt.ylim(ymax, ymin)
    plt.xlim(-0.1, double_phase + 1.1)
    plt.xlabel(f"{x_col}")
    plt.ylabel(f"{y_col}")
    plt.title(f"{object=} {filter=} {vtype=} {median_mag=:.3f} {mad=:.3f} {period=:.6f}")

    plt.savefig(output_dir / f"{object}_{filter}_{vtype}.png")
    plt.clf()
    plt.close()
