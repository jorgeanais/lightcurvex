from pathlib import Path

from src.data.loader import load_catalogs, load_RRLyrae
from src.extractor.gather import gather_data
from src.extractor.load import save_to_files


DATA_PATH = "/home/jorge/Documents/data/CASU_411/tables/ascii_tables/"


def main() -> None:
    
    # Load catalogs
    rrlyrae = load_RRLyrae(Path(r"assets/J_A+A_638_A104_t411.vot"))
    catalogs = load_catalogs(Path(DATA_PATH))
    
    # Generate a table with common gathered data
    data = gather_data(rrlyrae, catalogs)

    # Save data
    save_to_files(data, DATA_PATH / "output")
    
    



if __name__ == "__main__":
    main()