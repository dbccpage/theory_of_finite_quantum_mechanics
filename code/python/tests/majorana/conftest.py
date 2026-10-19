import sys
from pathlib import Path

_SRC_MAJ = Path(__file__).resolve().parents[2] / 'src' / 'majorana'
if str(_SRC_MAJ) not in sys.path:
    sys.path.insert(0, str(_SRC_MAJ))
