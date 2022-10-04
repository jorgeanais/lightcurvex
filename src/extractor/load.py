from pathlib import Path


from astropy.table import Table



def save_to_files(table: Table, output_dir: Path, id_col: str = "GaiaDR2") -> None:
    """Save data to a folder"""

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    # Save data
    table.write(output_dir / "data.vot", overwrite=True, format="votable")
    
    df = table.to_pandas()
    ids = list(df[id_col].unique())

    # Save objects independently
    for id in ids:
        df.query(f"{id_col} == {id}").to_csv(output_dir / f"{id}.csv", index=False)
