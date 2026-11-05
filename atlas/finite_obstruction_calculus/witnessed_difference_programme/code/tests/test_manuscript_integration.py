"""The canonical manuscript holds the accepted proofs, not links to them."""

import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parents[1]
PAPER = CODE_DIR.parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from observer_completion.distinct_replay import (  # noqa: E402
    check_inertia_promotion,
    check_readout_bound,
)


ANCHORS = (
    "Theorem L1 (sharp admitted-error recovery)",
    "Both selection and verification terminate by finite enumeration",
    "Theorem L2 (minimum linear observer completion)",
    "Theorem L3 (local readout bound)",
    "Theorem L4.",
    "Theorem T1 (full consistency, explicit envelope)",
    r"A_\theta=L\{30(\theta+\theta^2)e^{16\theta}B^2",
    "Theorem T2.",
    "Corollary T3 (eventual finite positivity).",
    "Theorem T4 (adapter descent).",
    "WDP-DIM-1",
    "m_{\\mathrm{both}}=\\dim K-\\dim(K\\cap B)+\\dim T",
    "-1/706440",
    "-1/88305",
    "r=1/10",
    "outside the",
    "r\\le 1/192",
    "The converse is withdrawn.",
    "rows 1, 10, and 16",
)


def test_accepted_proofs_are_in_the_manuscript_not_linked_away():
    text = (PAPER / "witnessed_difference_programme.md").read_text(encoding="utf-8")
    for anchor in ANCHORS:
        assert anchor in text, anchor
        at = text.index(anchor)
        window = text[max(0, at - 180) : at + 240]
        assert "see file" not in window.lower()
        assert "see `" not in window.lower()
    appendix_u = text[text.index("## Appendix U"): text.index("## Appendix V")]
    assert "if and only if those rows have rank" not in appendix_u
    assert "every proper subspace still hides a weight-one error" not in appendix_u
    assert "e_2 and e_3" in text or "e_2,e_3" in text
    l1 = text.index("Theorem L1 (sharp admitted-error recovery)")
    assert "Proof." in text[l1 : l1 + 700]
    t1 = text.index("Theorem T1 (full consistency, explicit envelope)")
    assert "Proof, with conservative constants." in text[t1 : t1 + 500]
    check_inertia_promotion({"all_m_from_this_point": False})
    try:
        check_inertia_promotion({"all_m_from_this_point": True})
    except ValueError as error:
        assert str(error) == "finite_m_promoted_to_all_m"
    else:
        raise AssertionError("finite-M promotion was accepted")
    try:
        check_readout_bound({"upper_bound": "2*beta", "asserted_floor": "beta"})
    except ValueError as error:
        assert str(error) == "lr_upper_bound_as_error_floor"
    else:
        raise AssertionError("an upper bound was accepted as an error floor")
