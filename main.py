from pathlib import Path

from src.data.loader import load_catalogs, load_RRLyrae
from src.extractor.gather import gather_data
from src.processing.dephase import process_phase_folding
from src.processing.plots import plot_data
from src.processing.summary import summarize
from src.utils.write import save_to_file


DATA_PATH = Path("/home/jorge/Documents/data/CASU_411/tables/ascii_tables_no-tiled/")
OUTPUT_PATH = Path("/home/jorge/output/")


def main() -> None:

    # Load catalogs
    rrlyrae = load_RRLyrae(Path(r"assets/all_rrlyrae_t411.vot"))
    catalogs = load_catalogs(DATA_PATH)

    # Generate a table with common gathered data
    data = gather_data(rrlyrae, catalogs)

    # Phase folding
    data =  process_phase_folding(data)

    # Save data
    save_to_file(data, OUTPUT_PATH / "output_dephase")

    # Plot results
    plot_data(data, OUTPUT_PATH / "plots")

    # Add a data summary. How many objects, avg. epochs per filter, etc.
    # summarize(data.to_pandas(), OUTPUT_PATH / "summary")


if __name__ == "__main__":
    main()
