"""fivestar"""

from pathlib import Path

import dotenv

dotenv.load_dotenv(".env")

DATA_DIR = Path(__file__).parent.parent.joinpath("data")
DATA_DIR.joinpath("info").mkdir(exist_ok=True)
DATA_DIR.joinpath("reviews").mkdir(exist_ok=True)
DATA_DIR.joinpath("summaries").mkdir(exist_ok=True)
DATA_DIR.joinpath("summaries", "info").mkdir(exist_ok=True)
DATA_DIR.joinpath("summaries", "reviews").mkdir(exist_ok=True)
