"""QM-122 dual witnesses re-exported under the qm module namespace.

Origin: papers/foundations/finite_ledger.md claim QM-122-C38.
Claim: urn:omega:fqm:qm122:python-dual-of-named-lean-witnesses:v1
AuthorityEffect: None
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    from qm122_lib import exported_reversible_report_count
    from qm122_lib.qm122_dual import *
    from qm122_lib.qm122_dual import __all__ as _dual_all
except ImportError:
    _src = str(Path(__file__).resolve().parents[1])
    if _src not in sys.path:
        sys.path.insert(0, _src)
    from qm122_lib import exported_reversible_report_count
    from qm122_lib.qm122_dual import *
    from qm122_lib.qm122_dual import __all__ as _dual_all

__all__ = list(_dual_all) + ["exported_reversible_report_count"]
