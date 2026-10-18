//! Production runner for the MUB(6) finite-cover computation.
//!
//! `mub6_cover` is the branch-and-bound *engine* (certify | prune off-torus | split | recurse).
//! This module turns it into a *runnable* over the whole candidate space: it builds the
//! gauge-fixed candidate region, decomposes it into independent chunks for distributed
//! compute, merges the per-chunk reports, and emits a serializable `CoverCertificate` — the
//! artifact a large-compute run produces and that the Lean bridge `MUB.FiniteVectorCover`
//! (ENC-1148) consumes.
//!
//! ## The candidate region (gauge-fixed 5-torus)
//!
//! A fourth MU vector must be unbiased to `B1` (`|v_i|² = 1/6` ∀i), and global phase is gauge,
//! so WLOG `v_0 = 1/√6` (real, positive) and the candidate set is the 5-torus of phases
//! `(φ_1,…,φ_5)`. In real `(x_i, y_i)` coordinates: `x_0` brackets `1/√6` and `y_0 = 0`
//! (`gauge_fixed_torus_region`); each free `v_i` ranges over the bounding box of its circle
//! `x_i² + y_i² = 1/6` (`circle_box`), with off-circle sub-boxes pruned during the cover. All
//! endpoints rational — no transcendental angle enclosure.
//!
//! ## Distributing the run
//!
//! The branch-and-bound is embarrassingly parallel: `presplit_region` decomposes the region
//! into `2^depth` independent sub-regions, each covered by a separate `cover_region` call
//! (here folded sequentially via `cover_region_chunked`; for large compute the chunks are
//! farmed to separate threads/processes/machines and their `CoverReport`s merged with
//! `merge_reports`). A completed run with `complete = true` (no uncertified residue) is a
//! finite certified cover of the whole candidate torus.
//!
//! mints no authority. The full 5-torus run is a heavy (but finite) computation — the runner
//! and certificate format are here; the cover of a real lower-dimensional slice is exercised
//! in tests as the end-to-end validation.

use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Mutex;

use num_rational::BigRational;
use num_traits::ToPrimitive;
use serde::{Deserialize, Serialize};

use crate::omega_native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, ExactVec, D};
use crate::omega_native::census::mub6_claim_gate::certificate_from_exact_only;
use crate::omega_native::exact::mub6_cover::{
    box_touches_torus, cover_region, CoverReport, EnclosedTriple,
};
use crate::omega_native::exact::mub6_cyclotomic_enclosure::{cyc24_real_imag_enclosure, SqrtBox};
use crate::omega_native::exact::mub6_interval_cover::VectorBox;
use omega_kernel::interval::Interval;
use omega_number_theory::rational::ri;

/// Bounding interval `[-41/100, 41/100]` for a free circle coordinate: the circle has radius
/// `1/√6 ≈ 0.40825 < 0.41`, so the square `circle_box × circle_box` contains the whole circle.
pub fn circle_box() -> Interval {
    Interval::new(-ri(41) / ri(100), ri(41) / ri(100))
}

/// A tight rational bracket of `1/√6` for the gauge-fixed coordinate `x_0`
/// (`lo² ≤ 1/6 ≤ hi²`, checked in tests): `[4082/10000, 4083/10000]`.
pub fn r_bracket() -> Interval {
    Interval::new(ri(4082) / ri(10000), ri(4083) / ri(10000))
}

/// The gauge-fixed candidate region: `v_0` pinned real-positive at `1/√6`, `v_1..v_5` free
/// over their circles. This is the compact 5-torus a 4th MU vector must inhabit.
pub fn gauge_fixed_torus_region() -> VectorBox {
    let mut region: VectorBox = std::array::from_fn(|_| circle_box());
    region[0] = r_bracket(); // x_0 ≈ 1/√6
    region[1] = Interval::point(BigRational::from(num_bigint::BigInt::from(0))); // y_0 = 0 (gauge)
    region
}

/// The full (non-gauge-fixed) 6-torus region: every `v_i` free. A correctness superset of the
/// gauge-fixed region (one extra dimension); covering it also rules out all 4th MU vectors.
pub fn full_torus_region() -> VectorBox {
    std::array::from_fn(|_| circle_box())
}

fn split_widest(vbox: &VectorBox) -> (VectorBox, VectorBox) {
    let mut wi = 0;
    let mut width = vbox[0].hi() - vbox[0].lo();
    for i in 1..2 * D {
        let w = vbox[i].hi() - vbox[i].lo();
        if w > width {
            width = w;
            wi = i;
        }
    }
    let (left, right) = vbox[wi].bisect_closed();
    debug_assert_eq!(left.hi(), right.lo());
    debug_assert!(left.contains(left.hi()));
    debug_assert!(right.contains(right.lo()));
    let mut a = vbox.clone();
    let mut b = vbox.clone();
    a[wi] = left;
    b[wi] = right;
    (a, b)
}

/// Decompose `region` into `2^depth` independent sub-regions (repeatedly bisecting the widest
/// coordinate). Their union is exactly `region`, so covering all of them covers `region` —
/// the unit of distribution for a large-compute run.
pub fn presplit_region(region: VectorBox, depth: u32) -> Vec<VectorBox> {
    let mut chunks = vec![region];
    for _ in 0..depth {
        let mut next = Vec::with_capacity(chunks.len() * 2);
        for c in chunks {
            let (a, b) = split_widest(&c);
            next.push(a);
            next.push(b);
        }
        chunks = next;
    }
    chunks
}

fn empty_report() -> CoverReport {
    CoverReport {
        certified: 0,
        off_torus: 0,
        uncertified: Vec::new(),
        min_gap: None,
        max_depth_used: 0,
    }
}

/// Merge two cover reports (the reduction a distributed run performs over its chunks).
pub fn merge_reports(mut a: CoverReport, b: CoverReport) -> CoverReport {
    a.certified += b.certified;
    a.off_torus += b.off_torus;
    a.uncertified.extend(b.uncertified);
    a.min_gap = match (a.min_gap.take(), b.min_gap) {
        (Some(x), Some(y)) => Some(if x <= y { x } else { y }),
        (Some(x), None) => Some(x),
        (None, y) => y,
    };
    a.max_depth_used = a.max_depth_used.max(b.max_depth_used);
    a
}

/// Cover `region` by first decomposing into `2^presplit_depth` chunks (the distribution unit)
/// then covering each to `max_depth` and merging. Sequential reference implementation; for
/// large compute the per-chunk `cover_region` calls are the parallel/distributed work items.
pub fn cover_region_chunked(
    enc: &EnclosedTriple,
    region: VectorBox,
    presplit_depth: u32,
    max_depth: u32,
) -> CoverReport {
    presplit_region(region, presplit_depth)
        .into_iter()
        .map(|chunk| cover_region(enc, chunk, max_depth))
        .fold(empty_report(), merge_reports)
}

// ----------------------------------------------------------------------------------------
// f64 prefilter — the fast guide that makes a CPU run feasible (and is the GPU-able kernel).
//
// Exact `BigRational` certification is the cost. Most boxes during a descent are nowhere near
// the critical manifold and will be subdivided regardless; computing their *exact* residual is
// wasted. The prefilter computes a cheap f64 interval estimate of the obstruction; the exact
// certificate is invoked ONLY when the estimate is plausibly positive (or at max depth).
// Soundness is unchanged: every certified box is confirmed by the exact `certify`; the f64
// only decides *when to attempt* it. This is exactly the kernel that GPU-parallelizes (f64
// interval arithmetic over millions of boxes, exact confirmation only on the survivors).
// ----------------------------------------------------------------------------------------

fn mul_iv(a: (f64, f64), b: (f64, f64)) -> (f64, f64) {
    let p = [a.0 * b.0, a.0 * b.1, a.1 * b.0, a.1 * b.1];
    (
        p.iter().cloned().fold(f64::INFINITY, f64::min),
        p.iter().cloned().fold(f64::NEG_INFINITY, f64::max),
    )
}

fn sq_iv(a: (f64, f64)) -> (f64, f64) {
    if a.0 >= 0.0 {
        (a.0 * a.0, a.1 * a.1)
    } else if a.1 <= 0.0 {
        (a.1 * a.1, a.0 * a.0)
    } else {
        (0.0, (a.0 * a.0).max(a.1 * a.1))
    }
}

/// f64 image of the enclosed triple: each fixed-vector entry's conjugate as `(A_lo, A_hi, B_lo,
/// B_hi)`. A heuristic guide for subdivision — never a certificate.
pub struct EnclosedTripleF64 {
    cols: Vec<[(f64, f64, f64, f64); D]>,
}

impl EnclosedTripleF64 {
    pub fn standard() -> Self {
        Self::from_exact_columns(&canonical_triple_exact())
    }

    /// f64 prefilter enclosure of an arbitrary exact triple (heuristic only; never a certificate).
    pub fn from_exact_columns(columns: &[ExactVec]) -> Self {
        let sb = SqrtBox::standard();
        let cols = columns
            .iter()
            .map(|e| {
                std::array::from_fn(|k| {
                    let (a, b) = cyc24_real_imag_enclosure(&e[k].conj(), &sb);
                    (
                        a.lo().to_f64().unwrap(),
                        a.hi().to_f64().unwrap(),
                        b.lo().to_f64().unwrap(),
                        b.hi().to_f64().unwrap(),
                    )
                })
            })
            .collect();
        EnclosedTripleF64 { cols }
    }

    /// The f64 prefilter for the moduli-neighborhood cover: widen each `B2`/`B3` entry by
    /// `±delta` (`B1` columns `0..6` exact), matching `EnclosedTriple::widened`. The prefilter is
    /// only a heuristic guide for *when* to attempt the exact certificate, so soundness does not
    /// depend on it; widening keeps it well-matched to the widened exact triple.
    pub fn widened(delta: f64) -> Self {
        Self::widened_from_exact_columns(&canonical_triple_exact(), delta)
    }

    /// f64 prefilter matching [`EnclosedTriple::widened_from_exact_columns`] for an arbitrary
    /// exact triple center. Heuristic only — never a certificate.
    pub fn widened_from_exact_columns(columns: &[ExactVec], delta: f64) -> Self {
        let base = Self::from_exact_columns(columns);
        let cols = base
            .cols
            .iter()
            .enumerate()
            .map(|(ci, col)| {
                std::array::from_fn(|k| {
                    let (a_lo, a_hi, b_lo, b_hi) = col[k];
                    if ci < D {
                        (a_lo, a_hi, b_lo, b_hi)
                    } else {
                        (a_lo - delta, a_hi + delta, b_lo - delta, b_hi + delta)
                    }
                })
            })
            .collect();
        EnclosedTripleF64 { cols }
    }

    /// Non-rigorous f64 lower-bound estimate of `∑_i ω_i²` over the box (heuristic guide only).
    pub fn residual_lower_estimate(&self, vbox: &VectorBox) -> f64 {
        let sixth = 1.0 / 6.0;
        let xy: Vec<(f64, f64)> = (0..2 * D)
            .map(|i| {
                (
                    vbox[i].lo().to_f64().unwrap(),
                    vbox[i].hi().to_f64().unwrap(),
                )
            })
            .collect();
        let mut total = 0.0;
        for col in &self.cols {
            let (mut re, mut im) = ((0.0, 0.0), (0.0, 0.0));
            for k in 0..D {
                let (a_lo, a_hi, b_lo, b_hi) = col[k];
                let a = (a_lo, a_hi);
                let b = (b_lo, b_hi);
                let x = xy[2 * k];
                let y = xy[2 * k + 1];
                let ax = mul_iv(a, x);
                let by = mul_iv(b, y);
                re.0 += ax.0 - by.1;
                re.1 += ax.1 - by.0;
                let ay = mul_iv(a, y);
                let bx = mul_iv(b, x);
                im.0 += ay.0 + bx.0;
                im.1 += ay.1 + bx.1;
            }
            let rs = sq_iv(re);
            let is = sq_iv(im);
            let om = (rs.0 + is.0 - sixth, rs.1 + is.1 - sixth);
            total += sq_iv(om).0;
        }
        total
    }
}

/// Cover `region` with the f64 prefilter: invoke the exact certificate only when the f64
/// estimate is plausibly positive (or at max depth); otherwise subdivide directly. Sound —
/// every certified box is exactly confirmed.
pub fn cover_region_prefiltered(
    exact: &EnclosedTriple,
    fast: &EnclosedTripleF64,
    region: VectorBox,
    max_depth: u32,
) -> CoverReport {
    cover_region_prefiltered_with_estimate(
        exact,
        |vbox| fast.residual_lower_estimate(vbox),
        region,
        max_depth,
    )
}

/// Same cover as [`cover_region_prefiltered`], with the estimate supplied by the caller.
///
/// A lying estimate can only skip or request the exact check. The admitted certificate
/// is `certificate_from_exact_only` of `exact.certify`.
pub fn cover_region_prefiltered_with_estimate<F>(
    exact: &EnclosedTriple,
    estimate_of: F,
    region: VectorBox,
    max_depth: u32,
) -> CoverReport
where
    F: Fn(&VectorBox) -> f64,
{
    let margin = 1e-9;
    let mut stack = vec![(region, 0u32)];
    let mut report = empty_report();
    while let Some((vbox, depth)) = stack.pop() {
        if depth > report.max_depth_used {
            report.max_depth_used = depth;
        }
        if !box_touches_torus(&vbox) {
            report.off_torus += 1;
            continue;
        }
        let at_max = depth >= max_depth;
        let estimate = estimate_of(&vbox);
        let exact_cert = if estimate > margin || at_max {
            exact.certify(&vbox)
        } else {
            None
        };
        if let Some(c) = certificate_from_exact_only(exact_cert, estimate) {
            report.certified += 1;
            report.min_gap = Some(match report.min_gap.take() {
                Some(g) if g <= c.f_gap => g,
                _ => c.f_gap,
            });
            continue;
        }
        if at_max {
            report.uncertified.push(vbox);
        } else {
            let (a, b) = split_widest(&vbox);
            stack.push((a, depth + 1));
            stack.push((b, depth + 1));
        }
    }
    report
}

/// The production entry point: presplit into chunks (the distribution unit), cover each with
/// the f64-prefiltered exact cover, log progress to stderr (for long CPU runs), and merge.
/// Returns the merged report — `complete = true` ⟺ a finite certified cover of `region`.
pub fn run_cover(
    region: VectorBox,
    presplit_depth: u32,
    max_depth: u32,
    label: &str,
) -> CoverReport {
    let exact = EnclosedTriple::standard();
    let fast = EnclosedTripleF64::standard();
    let chunks = presplit_region(region, presplit_depth);
    let n = chunks.len();
    let mut acc = empty_report();
    for (i, chunk) in chunks.into_iter().enumerate() {
        let r = cover_region_prefiltered(&exact, &fast, chunk, max_depth);
        let (rc, ro, ru, rd) = (
            r.certified,
            r.off_torus,
            r.uncertified.len(),
            r.max_depth_used,
        );
        acc = merge_reports(acc, r);
        eprintln!(
            "[{label}] chunk {}/{n}: +{rc}c +{ro}o +{ru}u | total {}c {}o {}u depth{} maxd{rd}",
            i + 1,
            acc.certified,
            acc.off_torus,
            acc.uncertified.len(),
            acc.max_depth_used,
        );
    }
    acc
}

/// Parallel production entry: presplit into `2^presplit_depth` independent chunks (the
/// distribution unit) and farm them across `n_threads` worker threads via `std::thread::scope`
/// — no external dependency, no shared mutable cover state (each worker keeps a local report and
/// merges once at the end). The branch-and-bound is embarrassingly parallel, so the merged
/// report is **identical** to the sequential `run_cover` (`merge_reports` is associative and the
/// chunk set is fixed); only the wall-clock differs. `n_threads = 0` uses
/// `available_parallelism`. This is how the full 5-torus run finishes in minutes on many cores.
pub fn run_cover_parallel(
    region: VectorBox,
    presplit_depth: u32,
    max_depth: u32,
    label: &str,
    n_threads: usize,
) -> CoverReport {
    let exact = EnclosedTriple::standard();
    let fast = EnclosedTripleF64::standard();
    run_cover_parallel_with(
        &exact,
        &fast,
        region,
        presplit_depth,
        max_depth,
        label,
        n_threads,
    )
}

/// The moduli-neighborhood parallel cover: run the cover against a triple **widened by `delta`**
/// (every `B2`/`B3` entry enclosed in a `±delta` box, `B1` exact). A complete cover
/// (`uncertified = 0`) proves *no fourth mutually-unbiased vector for **any** triple within
/// `delta` of `T0`* — the first no-go that holds over a continuous family of triples, not just the
/// point `T0`. `delta = 0` recovers the exact `T0` run.
pub fn run_moduli_cover(
    delta: &BigRational,
    region: VectorBox,
    presplit_depth: u32,
    max_depth: u32,
    label: &str,
    n_threads: usize,
) -> CoverReport {
    let exact = EnclosedTriple::widened(delta);
    let fast = EnclosedTripleF64::widened(delta.to_f64().unwrap_or(0.0));
    run_cover_parallel_with(
        &exact,
        &fast,
        region,
        presplit_depth,
        max_depth,
        label,
        n_threads,
    )
}

/// Shared parallel cover core: cover `region` against the supplied (exact, f64) enclosed triples.
/// `run_cover_parallel` passes the standard `T0` enclosure; `run_moduli_cover` passes a widened
/// one. Identical to the sequential cover up to wall-clock (associative `merge_reports`, fixed
/// chunk set).
pub fn run_cover_parallel_with(
    exact: &EnclosedTriple,
    fast: &EnclosedTripleF64,
    region: VectorBox,
    presplit_depth: u32,
    max_depth: u32,
    label: &str,
    n_threads: usize,
) -> CoverReport {
    let chunks = presplit_region(region, presplit_depth);
    let n = chunks.len();
    let workers = if n_threads == 0 {
        std::thread::available_parallelism()
            .map(|p| p.get())
            .unwrap_or(1)
    } else {
        n_threads
    }
    .min(n.max(1));

    let next = AtomicUsize::new(0);
    let done = AtomicUsize::new(0);
    let merged = Mutex::new(empty_report());
    let chunks = &chunks;

    std::thread::scope(|s| {
        for _ in 0..workers {
            s.spawn(|| {
                let mut local = empty_report();
                loop {
                    let i = next.fetch_add(1, Ordering::Relaxed);
                    if i >= n {
                        break;
                    }
                    let r = cover_region_prefiltered(exact, fast, chunks[i].clone(), max_depth);
                    local = merge_reports(local, r);
                    let d = done.fetch_add(1, Ordering::Relaxed) + 1;
                    eprintln!("[{label}] chunk {d}/{n} done");
                }
                let mut g = merged.lock().unwrap();
                let acc = std::mem::replace(&mut *g, empty_report());
                *g = merge_reports(acc, local);
            });
        }
    });

    merged.into_inner().unwrap()
}

/// The serializable artifact a cover run emits — the data the Lean bridge consumes
/// (`complete = true` ⟺ the region is a finite certified cover with no uncertified residue).
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq)]
pub struct CoverCertificate {
    pub region_label: String,
    pub certified: usize,
    pub off_torus: usize,
    pub uncertified: usize,
    /// `true` ⟺ no uncertified residue: every candidate vector in the region is in a certified
    /// box (no fourth MU vector anywhere in the region).
    pub complete: bool,
    /// The smallest certified `1 - f` gap, as an exact rational string (tightness witness).
    pub min_gap: Option<String>,
    pub max_depth_used: u32,
}

impl CoverReport {
    /// Summarize the report into the serializable cover certificate.
    pub fn certificate(&self, region_label: &str) -> CoverCertificate {
        CoverCertificate {
            region_label: region_label.to_string(),
            certified: self.certified,
            off_torus: self.off_torus,
            uncertified: self.uncertified.len(),
            complete: self.is_complete(),
            min_gap: self.min_gap.as_ref().map(|g| g.to_string()),
            max_depth_used: self.max_depth_used,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn sixth() -> BigRational {
        ri(1) / ri(6)
    }

    #[test]
    fn lying_float_estimate_cannot_outrun_the_exact_cover() {
        let exact = EnclosedTriple::standard();
        let region: VectorBox = std::array::from_fn(|_| Interval::new(ri(0), ri(1)));
        let depth = 2u32;
        let exact_report = cover_region(&exact, region.clone(), depth);
        let high = cover_region_prefiltered_with_estimate(&exact, |_| 1.0e9, region.clone(), depth);
        let low = cover_region_prefiltered_with_estimate(&exact, |_| -1.0e9, region, depth);
        assert_eq!(high.certified, exact_report.certified);
        assert!(low.certified <= exact_report.certified);
        assert!(!(high.is_complete() && !exact_report.is_complete()));
        assert!(!(low.is_complete() && !exact_report.is_complete()));
        assert!(!high.certificate("wide").complete || exact_report.is_complete());
    }

    #[test]
    fn r_bracket_brackets_inv_sqrt6() {
        let b = r_bracket();
        // lo² ≤ 1/6 ≤ hi²: the bracket soundly contains 1/√6.
        assert!(b.lo() * b.lo() <= sixth());
        assert!(b.hi() * b.hi() >= sixth());
    }

    #[test]
    fn gauge_fixed_region_touches_torus() {
        assert!(box_touches_torus(&gauge_fixed_torus_region()));
    }

    #[test]
    fn presplit_yields_independent_chunks() {
        let chunks = presplit_region(full_torus_region(), 4);
        assert_eq!(chunks.len(), 16);
        // every chunk lies within the original region bounds.
        let region = full_torus_region();
        for c in &chunks {
            for i in 0..2 * D {
                assert!(c[i].lo() >= region[i].lo() && c[i].hi() <= region[i].hi());
            }
        }
    }

    #[test]
    fn chunked_cover_of_a_torus_cell_is_complete() {
        // The chunked runner (presplit -> per-chunk cover -> merge) on a torus cell: every
        // chunk certifies, the merged report is complete (no uncertified residue) and carries a
        // positive gap. Validates the distribution path end-to-end on a fast region.
        let enc = EnclosedTriple::standard();
        let pin = Interval::new(ri(27) / ri(100), ri(29) / ri(100)); // [0.27,0.29] ~ torus point
        let region: VectorBox = std::array::from_fn(|_| pin.clone());
        let report = cover_region_chunked(&enc, region, 3, 24); // 8 chunks
        let cert = report.certificate("torus_cell");
        // Complete = no uncertified residue; every chunk is either certified or pruned as
        // off-torus (bisecting a coordinate can drop a chunk's |v_i|^2 range below 1/6).
        assert!(report.is_complete(), "cell fully covered: {cert:?}");
        assert!(
            report.certified + report.off_torus >= 8,
            "all chunks accounted: {cert:?}"
        );
        assert!(
            report.certified >= 1,
            "some chunk certified on-torus: {cert:?}"
        );
        assert!(report.min_gap.is_some());
    }

    #[test]
    fn widened_residual_is_a_sound_superset() {
        // Widening B2/B3 entries can only widen the residual interval, so the moduli (widened)
        // lower bound is <= the exact T0 lower bound on any box — a strictly sound test over a
        // superset of the valid MUB triples near T0.
        let exact = EnclosedTriple::standard();
        let wide = EnclosedTriple::widened(&(ri(1) / ri(1000)));
        let pin = Interval::new(ri(27) / ri(100), ri(29) / ri(100));
        let vbox: VectorBox = std::array::from_fn(|_| pin.clone());
        assert!(
            wide.residual_sq_lower(&vbox) <= exact.residual_sq_lower(&vbox),
            "widened bound is a sound lower bound (<= exact)"
        );
    }

    #[test]
    fn moduli_cover_of_a_cell_is_complete() {
        // A small moduli neighborhood (delta = 1/10000) of T0 over a torus cell still covers
        // completely: no fourth MU vector with these phases, for ANY triple within delta of T0.
        let report = run_moduli_cover(
            &(ri(1) / ri(10000)),
            std::array::from_fn(|_| Interval::new(ri(27) / ri(100), ri(29) / ri(100))),
            2,
            28,
            "moduli_cell",
            2,
        );
        assert!(
            report.is_complete(),
            "{:?}",
            report.certificate("moduli_cell")
        );
        assert!(report.certified >= 1);
    }

    /// Cheap characterization of how far the no-go extends into the moduli: cover a `k=3` torus
    /// slice at a range of neighborhood radii `delta = 1/den` and report which still complete.
    /// `cargo test -p omega_mub --release -- --ignored --nocapture moduli_delta_sweep`.
    #[test]
    #[ignore = "moduli neighborhood radius characterization"]
    fn moduli_delta_sweep() {
        for den in [1_000_000i64, 100_000, 10_000, 3_000, 1_000, 300, 100, 30] {
            let delta = ri(1) / ri(den);
            let label = format!("k3_delta_1_{den}");
            let report = run_moduli_cover(&delta, k_torus_region(3), 6, 48, &label, 0);
            let cert = report.certificate(&label);
            eprintln!(
                "MODULI delta=1/{den}: complete={} certified={} off_torus={} uncertified={}",
                cert.complete, cert.certified, cert.off_torus, cert.uncertified
            );
        }
    }

    /// Wall diagnostic: is a cover *failure* at radius `delta` interval **slop** (the true
    /// obstruction is positive — more depth completes it) or **structural** (the widened box
    /// contains a near-mutually-unbiased configuration, so no depth helps)? Runs the `k`-slice at
    /// increasing depth; for any uncertified boxes it reports the smallest **f64** residual
    /// estimate over them — clearly `> 0` ⟹ exact-interval slop (f64 sees positivity the
    /// rational interval lost), `≈ 0` or `< 0` ⟹ a genuine near-MU config (recall that
    /// independent `±delta` widening admits *non-MUB* configurations, which can host MU vectors).
    /// `MUB_WALL_DELTA_DEN` (default 30), `MUB_WALL_K` (default 3).
    /// `MUB_WALL_DELTA_DEN=30 cargo test -p omega_mub --release -- --ignored --nocapture moduli_wall_probe`.
    #[test]
    #[ignore = "moduli wall diagnostic: interval slop vs structural near-MU configuration"]
    fn moduli_wall_probe() {
        let den: i64 = std::env::var("MUB_WALL_DELTA_DEN")
            .ok()
            .and_then(|s| s.parse().ok())
            .unwrap_or(30);
        let k: usize = std::env::var("MUB_WALL_K")
            .ok()
            .and_then(|s| s.parse().ok())
            .unwrap_or(3);
        let delta = ri(1) / ri(den);
        let fast = EnclosedTripleF64::widened(delta.to_f64().unwrap());
        for depth in [48u32, 64] {
            let report =
                run_moduli_cover(&delta, k_torus_region(k), (2 * k) as u32, depth, "wall", 0);
            let min_est = report
                .uncertified
                .iter()
                .map(|b| fast.residual_lower_estimate(b))
                .fold(f64::INFINITY, f64::min);
            eprintln!(
                "WALL delta=1/{den} k={k} depth={depth}: complete={} certified={} uncertified={} min_uncert_f64_resid={:.3e}",
                report.is_complete(),
                report.certified,
                report.uncertified.len(),
                min_est
            );
            if report.is_complete() {
                break;
            }
        }
    }

    /// The headline run: the full gauge-fixed 5-torus, covered against a triple **widened by
    /// `delta`** — a complete cover proves no fourth MU vector for ANY triple within `delta` of
    /// `T0`. `delta = 1/MUB_MODULI_DELTA_DEN` (default `1/1000`). Emits the `CoverCertificate`.
    /// `MUB_MODULI_DELTA_DEN=1000 cargo test -p omega_mub --release -- --ignored --nocapture full_5_torus_moduli_cover`.
    #[test]
    #[ignore = "heavy: full 5-torus moduli-neighborhood cover (run on dedicated compute)"]
    fn full_5_torus_moduli_cover() {
        let den: i64 = std::env::var("MUB_MODULI_DELTA_DEN")
            .ok()
            .and_then(|s| s.parse().ok())
            .unwrap_or(1000);
        let delta = ri(1) / ri(den);
        let label = format!("gauge_fixed_5_torus_moduli_delta_1_{den}");
        let report = run_moduli_cover(&delta, gauge_fixed_torus_region(), 8, 64, &label, 0);
        let cert = report.certificate(&label);
        eprintln!(
            "COVER_CERTIFICATE {}",
            serde_json::to_string(&cert).unwrap()
        );
        assert!(
            report.is_complete(),
            "5-torus moduli neighborhood fully covered: {cert:?}"
        );
    }

    #[test]
    fn certificate_round_trips_through_json() {
        let enc = EnclosedTriple::standard();
        let pin = Interval::new(ri(27) / ri(100), ri(29) / ri(100));
        let region: VectorBox = std::array::from_fn(|_| pin.clone());
        let report = cover_region_chunked(&enc, region, 1, 24);
        let cert = report.certificate("cell");
        let json = serde_json::to_string(&cert).unwrap();
        let back: CoverCertificate = serde_json::from_str(&json).unwrap();
        assert_eq!(cert, back);
        assert!(cert.complete);
    }

    #[test]
    fn prefiltered_cover_agrees_with_exact_and_is_complete() {
        // The f64-prefiltered cover must reach the same verdict as the pure-exact cover on a
        // torus cell: complete, with the same certified/off-torus accounting. The prefilter
        // only changes WHEN the exact check runs, never the result.
        let exact = EnclosedTriple::standard();
        let fast = EnclosedTripleF64::standard();
        let pin = Interval::new(ri(27) / ri(100), ri(29) / ri(100));
        let region: VectorBox = std::array::from_fn(|_| pin.clone());
        let pre = cover_region_prefiltered(&exact, &fast, region.clone(), 24);
        let ex = cover_region(&exact, region, 24);
        assert!(pre.is_complete() && ex.is_complete());
        assert_eq!(pre.certified, ex.certified);
        assert_eq!(pre.off_torus, ex.off_torus);
        assert!(pre.min_gap.is_some());
    }

    #[test]
    fn run_cover_on_a_cell_is_complete() {
        // The production `run_cover` entry (presplit + prefilter + progress + merge) on a cell.
        let report = run_cover(
            std::array::from_fn(|_| Interval::new(ri(27) / ri(100), ri(29) / ri(100))),
            2,
            24,
            "cell",
        );
        assert!(report.is_complete(), "{:?}", report.certificate("cell"));
        assert!(report.certified >= 1);
    }

    #[test]
    fn parallel_cover_agrees_with_sequential() {
        // The multi-threaded runner must reach the EXACT same merged verdict as the sequential
        // `run_cover` on a region (the chunk set is fixed and `merge_reports` is associative, so
        // parallelism changes only wall-clock). A k=2 torus slice exercises real on/off-torus
        // chunks. Run with several workers on the same presplit.
        let region = k_torus_region(2);
        let seq = run_cover(region.clone(), 4, 32, "seq");
        let par = run_cover_parallel(region, 4, 32, "par", 4);
        assert_eq!(seq.certified, par.certified, "certified counts match");
        assert_eq!(seq.off_torus, par.off_torus, "off-torus counts match");
        assert_eq!(
            seq.uncertified.len(),
            par.uncertified.len(),
            "uncertified counts match"
        );
        assert_eq!(seq.is_complete(), par.is_complete());
        assert_eq!(seq.min_gap, par.min_gap, "tightest gap matches");
    }

    /// The full gauge-fixed 5-torus run, **parallelized** across worker threads — the heavy
    /// computation finished in minutes on many cores. Emits the `CoverCertificate` JSON.
    /// `cargo test -p omega_mub --release -- --ignored --nocapture full_5_torus_cover_parallel`.
    #[test]
    #[ignore = "heavy: full 5-torus cover, parallel (run on dedicated compute)"]
    fn full_5_torus_cover_parallel() {
        let report =
            run_cover_parallel(gauge_fixed_torus_region(), 8, 64, "gauge_fixed_5_torus", 0);
        let cert = report.certificate("gauge_fixed_5_torus");
        eprintln!(
            "COVER_CERTIFICATE {}",
            serde_json::to_string(&cert).unwrap()
        );
        assert!(report.is_complete(), "5-torus fully covered: {cert:?}");
    }

    /// A genuine 1-dimensional cross-section of the candidate torus: `v_0` gauge-fixed,
    /// `v_2..v_5` pinned near torus points, and `v_1` swept over its FULL circle. The driver
    /// prunes the off-circle bulk of `v_1`'s square and certifies every on-circle arc — a
    /// complete certified cover ⟹ no fourth MU vector with these phases and ANY `φ_1`. Heavy
    /// (full-circle sweep in exact arithmetic), so `#[ignore]`d; run on dedicated compute via
    /// `cargo test -p omega_mub -- --ignored one_torus_slice`.
    #[test]
    #[ignore = "heavy: full-circle one-torus slice (run on dedicated compute)"]
    fn one_torus_slice_full_circle() {
        let pin = Interval::new(ri(27) / ri(100), ri(29) / ri(100));
        let mut region: VectorBox = std::array::from_fn(|_| pin.clone());
        region[0] = r_bracket();
        region[1] = Interval::point(BigRational::from(num_bigint::BigInt::from(0)));
        region[2] = circle_box(); // v_1 free: full circle
        region[3] = circle_box();
        assert!(box_touches_torus(&region));
        let report = run_cover(region, 4, 48, "one_torus_slice");
        let cert = report.certificate("one_torus_slice");
        eprintln!("{}", serde_json::to_string(&cert).unwrap());
        assert!(report.is_complete(), "slice fully covered: {cert:?}");
        assert!(report.off_torus > 0);
    }

    /// The full gauge-fixed 5-torus run — the heavy computation intended for large compute
    /// (`cargo test -p omega_mub -- --ignored --nocapture full_5_torus`). The f64 prefilter
    /// makes the descent cheap; the exact certificate confirms every certified box. Emits the
    /// `CoverCertificate` JSON.
    #[test]
    #[ignore = "heavy: full 5-torus cover (run on dedicated compute)"]
    fn full_5_torus_cover() {
        let report = run_cover(gauge_fixed_torus_region(), 8, 64, "gauge_fixed_5_torus");
        let cert = report.certificate("gauge_fixed_5_torus");
        eprintln!("{}", serde_json::to_string(&cert).unwrap());
        assert!(report.is_complete(), "5-torus fully covered: {cert:?}");
    }

    /// A `k`-torus slice: `v_0` gauge-fixed, `v_1..v_k` swept over their FULL circles, the rest
    /// pinned. Covering it completely rules out a 4th MU vector over that `k`-dimensional
    /// cross-section. Used to characterize how the exact cover scales with free dimension
    /// (`cargo test -p omega_mub -- --ignored --nocapture torus_scaling`).
    fn k_torus_region(k: usize) -> VectorBox {
        let pin = Interval::new(ri(27) / ri(100), ri(29) / ri(100));
        let mut region: VectorBox = std::array::from_fn(|_| pin.clone());
        region[0] = r_bracket();
        region[1] = Interval::point(BigRational::from(num_bigint::BigInt::from(0)));
        for j in 1..=k {
            region[2 * j] = circle_box();
            region[2 * j + 1] = circle_box();
        }
        region
    }

    #[test]
    #[ignore = "scaling characterization across free torus dimension"]
    fn torus_scaling() {
        for k in 1..=3 {
            let t = std::time::Instant::now();
            let label = format!("{k}_torus");
            let report = run_cover(k_torus_region(k), (2 * k) as u32, 48, &label);
            let secs = t.elapsed().as_secs_f64();
            let cert = report.certificate(&label);
            eprintln!(
                "SCALING k={k}: complete={} certified={} off_torus={} uncertified={} time={:.1}s",
                cert.complete, cert.certified, cert.off_torus, cert.uncertified, secs
            );
        }
    }
}
