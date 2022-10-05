import pandas as pd
from astropy.table import Table
import matplotlib.pyplot as plt
from pathlib import Path


def plot_data(table: Table, output_dir: Path, id_col: str = "GaiaDR2", filter_col: str = "filter") -> None:

    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    
    df = table.to_pandas()
    ids = list(df[id_col].unique())

    # Save objects independently
    for id in ids:
        single_object_df = df.query(f"{id_col} == {id}").copy()
        filters = list(single_object_df[filter_col].unique())
        for f in filters:
            single_filter_object_df = single_object_df.query(f"{filter_col} == '{f}'").copy()
            plot_variable(single_filter_object_df, output_dir)


def plot_variable(
    df: pd.DataFrame,
    output_dir: Path,
    date_col: str = "mjd",
    mag_col: str = "mag", 
    mag_err_col: str = "mag_err",
    filter_col: str = "filter",
    vctype_col: str = "VCtype",
) -> None:
    """Plot a variable"""

    # Prepare data
    if mag_col == "date":
        df[date_col] = pd.to_datetime(df[date_col])

    object = df['GaiaDR2'].unique()[0]
    filter = df[filter_col].unique()[0]
    vctype = df[vctype_col].unique()[0]
    avg_mag = df[mag_col].mean()

    plt.figure(figsize=(10,8))
    plt.plot(df[date_col], df[mag_col], "o")
    plt.xlabel("Date (MJD)")
    plt.ylabel("Magnitude")
    plt.title(f"{object=} {filter=} {vctype=} {avg_mag=:.2f}")

    plt.savefig(output_dir / f"{object}_{filter}_{vctype}.png")
    plt.clf()
    plt.close()