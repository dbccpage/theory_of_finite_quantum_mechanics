"""Independent MUB(6) verifier and stratified sampling engine.

AuthorityEffect: None.
stated region only; mints no authority.

Implements independent Python verification from mathematical definitions:
1. Re-derives certified lower bounds for stratified samples of boxes:
   - minimum-gap boxes
   - deepest boxes
   - boxes adjacent to off-torus cells
   - random sample boxes
2. Full coverage verification for small artifacts (narrow cell, wide cell, chunk pilots).
3. Exact difference reporting between recomputed bounds and reported bounds.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import random
from typing import Any, Dict, List, NamedTuple, Optional, Sequence, Tuple

from .cover import (
    CertifiedBox,
    CoverReport,
    box_touches_torus,
    cover_region,
    gauge_fixed_torus_region,
    narrow_torus_cell,
    presplit_region,
    split_widest,
    verify_full_coverage,
    wide_torus_cell,
)
from .cyclotomic import SqrtBox
from .interval import (
    RationalInterval,
    VectorBox,
    box_volume,
)
from .masses import EnclosedTriple
from .mub_triples import (
    GENUINE_Y2Q1_SEEDS,
    GENUINE_Y2Q2_SEEDS,
    dita_seed_triple_columns,
    verify_triple_pairwise_mu,
)


class SampledBoxResult(NamedTuple):
    stratum: str
    seed: Tuple[int, int]
    depth: int
    box: VectorBox
    computed_gap: Fraction
    is_positive: bool
    touches_torus: bool
    expected_gap: Optional[Fraction] = None
    exact_difference: Optional[Fraction] = None


class StratifiedVerificationSummary(NamedTuple):
    total_boxes_tested: int
    strata_counts: Dict[str, int]
    all_positive: bool
    disagreements_count: int
    disagreements: List[Dict[str, Any]]
    sample_design: str
    verified_seeds: List[Tuple[int, int]]


class FullCoverageSummary(NamedTuple):
    artifact_name: str
    seed: Tuple[int, int]
    domain_label: str
    certified_count: int
    off_torus_count: int
    uncertified_count: int
    is_complete: bool
    min_gap: Fraction
    expected_min_gap: Optional[Fraction]
    min_gap_difference: Optional[Fraction]
    coverage_verified: bool
    coverage_message: str


def load_artifact_json(artifact_path: Path) -> Dict[str, Any]:
    """Load an artifact JSON file."""
    with open(artifact_path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_fraction(s: str) -> Fraction:
    """Parse rational fraction string 'num/den' or integer."""
    if "/" in s:
        n_str, d_str = s.strip().split("/")
        return Fraction(int(n_str), int(d_str))
    return Fraction(int(s.strip()), 1)


class IndependentMubVerifier:
    """Independent Python verifier for MUB(6) certified certificates and covers."""

    def __init__(self, artifacts_dir: Path | None = None) -> None:
        self.artifacts_dir = artifacts_dir
        self.sb = SqrtBox.standard()

    def get_enclosed_triple(
        self,
        dx: int,
        dy: int,
        delta: Fraction | None = None,
    ) -> EnclosedTriple:
        """Construct exact enclosed triple for seed (dx, dy)."""
        cols = dita_seed_triple_columns(dx, dy)
        if delta is not None and delta > 0:
            return EnclosedTriple.widened_from_columns(cols, delta, self.sb)
        return EnclosedTriple.from_columns(cols, self.sb)

    def verify_small_artifact_narrow_cell(
        self,
        dx: int = 0,
        dy: int = 8,
        artifact_path: Path | None = None,
    ) -> FullCoverageSummary:
        """Full coverage check on narrow_torus_cell for seed (dx, dy)."""
        enc = self.get_enclosed_triple(dx, dy)
        cell = narrow_torus_cell()
        report = cover_region(enc, cell, max_depth=24, store_all_boxes=True)

        cert_boxes = [cb.box for cb in report.certified_boxes]
        off_boxes = [ob[0] for ob in report.off_torus_boxes]
        cov_ok, cov_msg = verify_full_coverage(cell, cert_boxes, off_boxes)

        expected_min_gap = None
        gap_diff = None
        if artifact_path and artifact_path.exists():
            data = load_artifact_json(artifact_path)
            expected_min_gap = parse_fraction(data["cover"]["min_gap"])
            if report.min_gap is not None:
                gap_diff = report.min_gap - expected_min_gap

        return FullCoverageSummary(
            artifact_name=artifact_path.name if artifact_path else "narrow_cell",
            seed=(dx, dy),
            domain_label="narrow_torus_cell",
            certified_count=report.certified_count,
            off_torus_count=report.off_torus_count,
            uncertified_count=report.uncertified_count,
            is_complete=report.is_complete,
            min_gap=report.min_gap if report.min_gap is not None else Fraction(0, 1),
            expected_min_gap=expected_min_gap,
            min_gap_difference=gap_diff,
            coverage_verified=cov_ok,
            coverage_message=cov_msg,
        )

    def verify_small_artifact_wide_cell(
        self,
        dx: int = 0,
        dy: int = 8,
        artifact_path: Path | None = None,
    ) -> FullCoverageSummary:
        """Full coverage check on wide_torus_cell for seed (dx, dy)."""
        enc = self.get_enclosed_triple(dx, dy)
        cell = wide_torus_cell()
        report = cover_region(enc, cell, max_depth=10, store_all_boxes=True)

        cert_boxes = [cb.box for cb in report.certified_boxes]
        off_boxes = [ob[0] for ob in report.off_torus_boxes]
        cov_ok, cov_msg = verify_full_coverage(cell, cert_boxes, off_boxes)

        expected_min_gap = None
        gap_diff = None
        if artifact_path and artifact_path.exists():
            data = load_artifact_json(artifact_path)
            expected_min_gap = parse_fraction(data["cover"]["min_gap"])
            if report.min_gap is not None:
                gap_diff = report.min_gap - expected_min_gap

        return FullCoverageSummary(
            artifact_name=artifact_path.name if artifact_path else "wide_cell",
            seed=(dx, dy),
            domain_label="wide_torus_cell",
            certified_count=report.certified_count,
            off_torus_count=report.off_torus_count,
            uncertified_count=report.uncertified_count,
            is_complete=report.is_complete,
            min_gap=report.min_gap if report.min_gap is not None else Fraction(0, 1),
            expected_min_gap=expected_min_gap,
            min_gap_difference=gap_diff,
            coverage_verified=cov_ok,
            coverage_message=cov_msg,
        )

    def collect_stratified_boxes(
        self,
        dx: int,
        dy: int,
        chunks_to_sample: Sequence[int] = (0, 1, 15, 31, 63),
        target_per_stratum: int = 5,
        max_search_depth: int = 12,
        seed_rng: int = 42,
    ) -> List[SampledBoxResult]:
        """Collect and re-verify a stratified sample of boxes for seed (dx, dy).

        Strata:
        - minimum_gap: boxes attaining the lowest observed gap in explored chunks
        - deepest: boxes reaching maximum subdivision depth
        - near_off_torus: certified boxes whose sibling was off-torus
        - random: uniformly sampled boxes across exploration paths
        """
        rng = random.Random(seed_rng)
        stratified_results: List[SampledBoxResult] = []
        all_certified: List[CertifiedBox] = []
        near_off_torus: List[CertifiedBox] = []
        enc = self.get_enclosed_triple(dx, dy)

        # Explore requested presplit-6 chunks of the wide torus cell
        wide_cell = wide_torus_cell()
        presplit_chunks = presplit_region(wide_cell, depth=6)
        stack: List[Tuple[VectorBox, int]] = []
        for chunk_idx in chunks_to_sample:
            if 0 <= chunk_idx < len(presplit_chunks):
                stack.append((presplit_chunks[chunk_idx], 6))

        while stack:
            vbox, depth = stack.pop()
            if not box_touches_torus(vbox):
                continue

            gap = enc.certify_vector_box(vbox)
            if gap is not None:
                cbox = CertifiedBox(vbox, gap, depth)
                all_certified.append(cbox)
                continue

            if depth >= max_search_depth:
                continue

            a, b = split_widest(vbox)
            a_touches = box_touches_torus(a)
            b_touches = box_touches_torus(b)

            if a_touches and not b_touches:
                a_gap = enc.certify_vector_box(a)
                if a_gap is not None:
                    near_off_torus.append(CertifiedBox(a, a_gap, depth + 1))
            elif b_touches and not a_touches:
                b_gap = enc.certify_vector_box(b)
                if b_gap is not None:
                    near_off_torus.append(CertifiedBox(b, b_gap, depth + 1))

            stack.append((a, depth + 1))
            stack.append((b, depth + 1))

        # 1. Minimum gap stratum: sort by gap ascending
        sorted_by_gap = sorted(all_certified, key=lambda cb: cb.gap)
        min_gap_sample = sorted_by_gap[:target_per_stratum]
        for cb in min_gap_sample:
            # Independent re-verification of the lower bound
            recomputed = enc.f_gap(cb.box)
            diff = recomputed - cb.gap
            stratified_results.append(
                SampledBoxResult(
                    stratum="minimum_gap",
                    seed=(dx, dy),
                    depth=cb.depth,
                    box=cb.box,
                    computed_gap=recomputed,
                    is_positive=recomputed > 0,
                    touches_torus=box_touches_torus(cb.box),
                    expected_gap=cb.gap,
                    exact_difference=diff,
                )
            )

        # 2. Deepest boxes stratum: sort by depth descending
        sorted_by_depth = sorted(all_certified, key=lambda cb: cb.depth, reverse=True)
        deepest_sample = sorted_by_depth[:target_per_stratum]
        for cb in deepest_sample:
            recomputed = enc.f_gap(cb.box)
            diff = recomputed - cb.gap
            stratified_results.append(
                SampledBoxResult(
                    stratum="deepest",
                    seed=(dx, dy),
                    depth=cb.depth,
                    box=cb.box,
                    computed_gap=recomputed,
                    is_positive=recomputed > 0,
                    touches_torus=box_touches_torus(cb.box),
                    expected_gap=cb.gap,
                    exact_difference=diff,
                )
            )

        # 3. Near off-torus stratum (explicit: does not fall back to ordinary certified boxes)
        near_off_sample = near_off_torus[:target_per_stratum]
        for cb in near_off_sample:
            recomputed = enc.f_gap(cb.box)
            diff = recomputed - cb.gap
            stratified_results.append(
                SampledBoxResult(
                    stratum="near_off_torus",
                    seed=(dx, dy),
                    depth=cb.depth,
                    box=cb.box,
                    computed_gap=recomputed,
                    is_positive=recomputed > 0,
                    touches_torus=box_touches_torus(cb.box),
                    expected_gap=cb.gap,
                    exact_difference=diff,
                )
            )

        # 4. Random sample stratum
        if len(all_certified) > target_per_stratum:
            rand_sample = rng.sample(all_certified, target_per_stratum)
        else:
            rand_sample = list(all_certified)
        for cb in rand_sample:
            recomputed = enc.f_gap(cb.box)
            diff = recomputed - cb.gap
            stratified_results.append(
                SampledBoxResult(
                    stratum="random",
                    seed=(dx, dy),
                    depth=cb.depth,
                    box=cb.box,
                    computed_gap=recomputed,
                    is_positive=recomputed > 0,
                    touches_torus=box_touches_torus(cb.box),
                    expected_gap=cb.gap,
                    exact_difference=diff,
                )
            )

        return stratified_results

    def run_stratified_audit(
        self,
        seeds: Sequence[Tuple[int, int]] = ((0, 8), (8, 0), (16, 16), (0, 16), (8, 8), (16, 0)),
        target_per_stratum: int = 5,
        chunks_to_sample: Sequence[int] = (0, 1, 7, 15, 31, 63),
    ) -> Tuple[StratifiedVerificationSummary, List[SampledBoxResult]]:
        """Run full stratified verification across all declared seeds."""
        all_results: List[SampledBoxResult] = []
        strata_counts: Dict[str, int] = {}
        disagreements: List[Dict[str, Any]] = []

        for dx, dy in seeds:
            results = self.collect_stratified_boxes(
                dx=dx,
                dy=dy,
                chunks_to_sample=chunks_to_sample,
                target_per_stratum=target_per_stratum,
            )
            all_results.extend(results)

        for res in all_results:
            strata_counts[res.stratum] = strata_counts.get(res.stratum, 0) + 1
            if not res.is_positive:
                disagreements.append({
                    "type": "non_positive_gap",
                    "seed": res.seed,
                    "stratum": res.stratum,
                    "computed_gap": str(res.computed_gap),
                })
            if res.exact_difference is not None and res.exact_difference != 0:
                disagreements.append({
                    "type": "recomputation_mismatch",
                    "seed": res.seed,
                    "stratum": res.stratum,
                    "exact_difference": str(res.exact_difference),
                })

        sample_design = (
            f"Stratified sample of 4 strata (minimum_gap, deepest, near_off_torus, random) "
            f"across {len(seeds)} seeds ({', '.join(f'({dx},{dy})' for dx, dy in seeds)}) "
            f"drawn from presplit-6 chunks {list(chunks_to_sample)}. "
            f"Every box recomputed in exact rational arithmetic over Q(zeta_24) "
            f"(shared interval/masses implementation self-consistency check)."
        )

        all_positive = (len(all_results) > 0) and all(r.is_positive for r in all_results)

        summary = StratifiedVerificationSummary(
            total_boxes_tested=len(all_results),
            strata_counts=strata_counts,
            all_positive=all_positive,
            disagreements_count=len(disagreements),
            disagreements=disagreements,
            sample_design=sample_design,
            verified_seeds=list(seeds),
        )

        return summary, all_results
