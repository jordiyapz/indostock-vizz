from pathlib import Path
from os.path import dirname, join


class PATH(Path):
    DATA: Path = Path(join(dirname(__file__), '../data'))
    DATASET: Path = None


PATH.DATASET = PATH.DATA
