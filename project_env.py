from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MYUTILS_ROOT = ROOT.parent / "myutils"

if str(MYUTILS_ROOT) not in sys.path:
    sys.path.insert(0, str(MYUTILS_ROOT))
