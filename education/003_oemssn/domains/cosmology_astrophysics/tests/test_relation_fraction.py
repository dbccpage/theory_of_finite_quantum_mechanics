"""Order statistics have no inferred physical dimension."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "code"))
from domain_cosmology_kernel import CausalSet
def test_relation_fraction_on_chain():
    p=CausalSet(["a","b","c"], {("a","b"),("b","c")})
    assert p.interval_relation_fraction("a","c") == 1
    assert p.interval_relation_fraction("c","a") is None


def test_order_receipt_reports_relation_fraction_not_dimension():
    p=CausalSet(["a","b","c"], {("a","b"),("b","c")})
    receipt=p.emit_receipt()
    assert receipt.interval_comparable_fraction == 1
    assert receipt.num_irreducible_links == 2
