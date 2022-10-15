import numpy as np
from pathlib import Path

from astropy.table import Table


def save_to_file(table: Table, output_dir: Path, id_col: str = "source_id") -> None:
    """Save the content of a table splited by id_col"""

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    # Save the entire table
    table.write(str(output_dir / "data.csv"), format="csv")

    
    # Save objects independently
    ids = list(np.unique(table[id_col]))
    for id in ids:
        table[table[id_col] == id].write(str(output_dir / f"{id}.csv"), format="csv")
