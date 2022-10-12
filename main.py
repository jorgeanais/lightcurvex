from pathlib import Path

from src.data.loader import load_catalogs, load_RRLyrae
from src.extractor.gather import gather_data
from src.extractor.plots import plot_data
from src.extractor.write import save_to_file


DATA_PATH = Path("/home/jorge/Documents/data/CASU_411/tables/ascii_tables_no-tiled/")


def main() -> None:

    # Load catalogs
    rrlyrae = load_RRLyrae(Path(r"assets/J_A+A_638_A104_t411.vot"))
    catalogs = load_catalogs(DATA_PATH)

    # Generate a table with common gathered data
    data = gather_data(rrlyrae, catalogs)

    # Save data
    save_to_file(data, DATA_PATH / "output")
    plot_data(data, DATA_PATH / "plots")

    # TODO: Add a data summary. How many objects, avg. epochs per filter, avg. mag per filter, RR Lyrae types, etc.


if __name__ == "__main__":
    main()
