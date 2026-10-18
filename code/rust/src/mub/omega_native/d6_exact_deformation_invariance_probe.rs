//! Phase-0 exact **deformation-invariance probe** for the MUB(6) fourth-vector problem,
//! over the native field `Q(zeta_24)`.
//!
//! This is the first module that actually *runs* the deformation-invariance bypass idea
//! (design: `omega_engine/research/published/012_mutually_unbiased_bases/mub6_deformation_invariance_bypass_scope.md`, §6) instead of describing
//! it. The bypass needs an obstruction invariant `I(T)` that is *simultaneously*
//!
//!   * **(a) no-go-certifying:** `I(T) != 0 ==> no fourth MU vector for T`, and
//!   * **(b) deformation-rigid:** `I` is locally constant across the moduli.
//!
//! We probe the two *cohomological* candidate invariants already built exactly in-tree —
//! `rank_j = rank(J)` (the tangent Jacobian rank) and `h1_dim = dim H^1` of the local
//! tangent-obstruction complex — by sweeping the candidate fourth-vector `v` over the
//! gauge-fixed candidate 5-torus of the FIXED canonical triple `T0`, and comparing against
//! two "far from flat" controls (`e_0`, `generic_unit`). Everything that decides a gate is
//! computed in exact `Cyc24` arithmetic; `f64` is used ONLY for the human-readable columns
//! (a real-part evaluation of a cyclotomic number) and never to decide a gate.
//!
//! Two gates:
//!
//!   * **Gate A (no-go link):** do `(rank_j, h1_dim)` DIFFER between the near-MU flat
//!     samples and the far controls? If the pair is identical regardless of how flat/near-MU
//!     `v` is, the cohomological invariant does not track the scalar no-go => Gate A FAIL.
//!   * **Gate B (rigidity / wall-crossing):** is `(rank_j, h1_dim)` CONSTANT across the flat
//!     5-torus samples, or does it jump? Flat samples whose pair differs from the modal value
//!     are the vector-level wall locus `W`.
//!
//! Terminal: `OpenResidual`. Phase 0 mints NO authority; it only decides which candidate
//! invariant survives.
//!
//! # Firewall
//!
//! this module can issue is `OpenResidual`.
//!
//! **Honest scope note:** This is the vector-level rigidity + no-go-link probe for the
//! FIXED triple T0 (sweeping the candidate fourth-vector over the gauge-fixed 5-torus). The
//! triple-level deformation-invariance across the moduli is NOT attempted here: T0 is
//! currently our only exact non-gauge MU triple (the gauge orbit is trivially invariant
//! because Psi_basis is gauge-invariant), so an exact triple-level deformation path needs a
//! second inequivalent exact MU triple we do not yet have — that gap is itself the first
//! Phase-0 finding.

use num_rational::BigRational;
use num_traits::ToPrimitive;

use crate::omega_native::exact::d6_exact_curvature_cochain::{
    abs_sq, as_rational, canonical_triple_exact, cmp_exact_real, curvature_c2, norm_sq,
    wall_functional, ExactVec,
};
use crate::omega_native::exact::d6_exact_obstruction_cohomology::obstruction_cohomology;
use crate::omega_native::exact::d6_exact_tangent_obstruction::tangent_obstruction;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

crate::fixture_set!(fixtures, "d6_exact_deformation_invariance_probe");

/// Rational scalar as an exact `Cyc24`.
fn rat(num: i64, den: i64) -> Cyc24 {
    Cyc24::rat(ri(num) / ri(den))
}

pub(crate) use crate::omega_native::exact::mub6_field::inv_sqrt6;

fn zero_vec() -> ExactVec {
    std::array::from_fn(|_| Cyc24::zero())
}

/// The first standard-basis vector `e_0` (a "far from flat" control that lies in B1).
pub(crate) fn unit_e0() -> ExactVec {
    let mut v = zero_vec();
    v[0] = Cyc24::rat(ri(1));
    v
}

/// A generic exact unit vector `(1/sqrt2)(e_0 + i e_1)` — the sibling modules' control.
/// `norm^2 = 1/2 + 1/2 = 1`.
pub(crate) fn generic_unit() -> ExactVec {
    let s = Cyc24::sqrt2().mul(&rat(1, 2)); // 1/sqrt2
    let mut v = zero_vec();
    v[0] = s.clone();
    v[1] = Cyc24::zeta24(6).mul(&s); // i / sqrt2
    v
}

/// A flat root-of-unity candidate on the gauge-fixed 5-torus:
/// `v_k = (1/sqrt6) * zeta_24^{a_k}`, so `|v_k|^2 = 1/6` exactly and `||v||^2 = 1`.
/// `a_0` is expected to be `0` (gauge-fix `v_0` real).
pub(crate) fn flat_candidate(exps: [i64; 6]) -> ExactVec {
    let s = inv_sqrt6();
    std::array::from_fn(|k| s.mul(&Cyc24::zeta24(exps[k] as i32)))
}

/// **Reporting-only** numeric real part of a cyclotomic number: evaluate
/// `sum_k a_k zeta^k` at `zeta = e^{2 pi i / 24}` and take the real part. Used ONLY for the
/// human-readable table columns; never to decide a gate. (Real cyclotomic numbers equal
/// their conjugates, so the imaginary part is numerically zero.)
pub(crate) fn numeric_re(z: &Cyc24) -> f64 {
    let mut acc = 0.0f64;
    for (k, a) in z.a.iter().enumerate() {
        let ak = a.to_f64().unwrap_or(f64::NAN);
        acc += ak * (std::f64::consts::PI * (k as f64) / 12.0).cos();
    }
    acc
}

/// Which regime a candidate belongs to.
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Debug)]
pub enum SampleCategory {
    /// A "far from flat" control (not a near-MU candidate).
    FarControl,
    /// A flat root-of-unity candidate on the gauge-fixed 5-torus.
    FlatTorus,
}

/// One computed row of the exact probe table.
#[derive(Clone, Debug)]
pub struct SampleRow {
    pub label: String,
    pub category: SampleCategory,
    /// `norm_sq(v) == 1` exactly (asserted true at construction).
    pub is_unit: bool,
    /// Wall functional `f(v) = 1 - (6/5) sum_i omega_i^2`, exact rational if it is rational.
    pub f_rational: Option<BigRational>,
    /// Reporting-only numeric real part of `f`.
    pub f_float: f64,
    /// Curvature mass `sum_i |omega_i|^2`, exact rational if it is rational.
    pub omega_mass_rational: Option<BigRational>,
    /// Reporting-only numeric real part of the curvature mass.
    pub omega_mass_float: f64,
    /// Gate-internal: the EXACT curvature mass `sum_i |omega_i|^2` in `Cyc24`. Used only for
    /// the exact "same scalar, different invariant" falsification in Gate A (never f64).
    pub omega_mass_exact: Cyc24,
    /// `rank(J)` — the tangent Jacobian rank (candidate invariant).
    pub rank_j: usize,
    /// `dim coker(J) = 18 - rank(J)` — the first-order obstruction dimension.
    pub coker_dim: usize,
    /// `dim H^1` of the local tangent-obstruction complex (candidate invariant).
    /// `None` if the chain complex identity d1 . d0 == 0 fails (R06).
    pub h1_dim: Option<usize>,
    /// `dim H^2`.
    pub h2_dim: usize,
    /// Phase gauge `i*v` lies exactly in `ker(J)` (structural check, must be true).
    pub phase_gauge_in_kernel: bool,
    /// Bianchi identity `d1 . d0 = 0` holds exactly (structural check, must be true).
    pub d1_after_d0_zero: bool,
}

impl SampleRow {
    /// The candidate cohomological invariant pair `(rank_j, h1_dim)`.
    pub fn invariant_pair(&self) -> (usize, Option<usize>) {
        (self.rank_j, self.h1_dim)
    }
}

/// The full Phase-0 probe report with both gate verdicts.
#[derive(Clone, Debug)]
pub struct ProbeReport {
    pub rows: Vec<SampleRow>,
    /// Gate A (no-go link): true iff the flat samples' invariant pairs DIFFER from the far
    /// controls' pairs (i.e. the invariant tracks the flat/near-MU regime).
    pub gate_a_pass: bool,
    pub gate_a_reason: String,
    /// Gate B (rigidity): true iff `(rank_j, h1_dim)` is CONSTANT across the flat samples.
    pub gate_b_pass: bool,
    pub gate_b_reason: String,
    /// Labels of flat samples whose invariant pair differs from the modal value (wall locus).
    pub wall_samples: Vec<String>,
    /// Phase-0's only terminal.
    pub terminal: &'static str,
}

/// Build the exact candidate set: two far controls plus the flat 5-torus samples.
pub(crate) fn candidate_set() -> Vec<(String, SampleCategory, ExactVec)> {
    let mut set: Vec<(String, SampleCategory, ExactVec)> = Vec::new();

    set.push(("e_0".to_string(), SampleCategory::FarControl, unit_e0()));
    set.push((
        "generic_unit".to_string(),
        SampleCategory::FarControl,
        generic_unit(),
    ));

    // Flat root-of-unity candidates on the gauge-fixed 5-torus (a_0 = 0).
    let tuples: [(&str, [i64; 6]); 12] = [
        ("flat_zeros", [0, 0, 0, 0, 0, 0]),
        ("flat_ramp1", [0, 1, 2, 3, 4, 5]),
        ("flat_ramp2", [0, 2, 4, 6, 8, 10]),
        ("flat_ramp3", [0, 3, 6, 9, 12, 15]),
        ("flat_ramp4", [0, 4, 8, 12, 16, 20]),
        ("flat_ramp5", [0, 5, 10, 15, 20, 1]),  // 25 mod 24 = 1
        ("flat_quad_sq", [0, 1, 4, 9, 16, 1]),  // i^2 mod 24 (25 mod 24 = 1)
        ("flat_tri", [0, 1, 3, 6, 10, 15]),     // triangular numbers
        ("flat_step6", [0, 6, 12, 18, 0, 6]),   // 6i mod 24
        ("flat_step8", [0, 8, 16, 0, 8, 16]),   // 8i mod 24
        ("flat_step12", [0, 12, 0, 12, 0, 12]), // 12i mod 24
        ("flat_quad_ii", [0, 2, 6, 12, 20, 6]), // i^2 + i mod 24 (30 mod 24 = 6)
    ];
    for (name, exps) in tuples {
        set.push((
            name.to_string(),
            SampleCategory::FlatTorus,
            flat_candidate(exps),
        ));
    }

    set
}

/// Compute one exact row for a candidate vector.
fn compute_row(
    columns: &[ExactVec],
    label: &str,
    category: SampleCategory,
    v: &ExactVec,
) -> SampleRow {
    // Exact unit-norm check (a construction invariant; asserted in the test harness).
    let is_unit = norm_sq(v) == Cyc24::rat(ri(1));

    let omega = curvature_c2(columns, v);

    // Exact curvature mass sum_i |omega_i|^2.
    let mut mass = Cyc24::zero();
    for w in &omega {
        mass = mass.add(&abs_sq(w));
    }
    let f = wall_functional(&omega);

    let tan = tangent_obstruction(columns, v).expect("the fixed triple has 18 vectors");
    let coho = obstruction_cohomology(columns, v);

    SampleRow {
        label: label.to_string(),
        category,
        is_unit,
        f_rational: as_rational(&f),
        f_float: numeric_re(&f),
        omega_mass_rational: as_rational(&mass),
        omega_mass_float: numeric_re(&mass),
        omega_mass_exact: mass,
        rank_j: tan.jacobian_rank,
        coker_dim: tan.obstruction_dim,
        h1_dim: coho.h1_dim,
        h2_dim: coho.h2_dim,
        phase_gauge_in_kernel: tan.phase_gauge_in_kernel,
        d1_after_d0_zero: coho.d1_after_d0_zero,
    }
}

/// Run the exact Phase-0 deformation-invariance probe on the **canonical** triple T0.
pub fn run_probe() -> ProbeReport {
    run_probe_on_columns(&canonical_triple_exact())
}

/// Run the Phase-0 vector-level probe on an arbitrary exact 18-column MU triple.
///
/// Used by the Q1 second-basepoint campaign: same Gate A/B logic, different carrier `T`.
/// Terminal remains `OpenResidual` — not a triple-level rigidity theorem.
pub fn run_probe_on_columns(columns: &[ExactVec]) -> ProbeReport {
    assert_eq!(
        columns.len(),
        super::d6_exact_curvature_cochain::COLUMN_COUNT,
        "probe expects 18 fixed columns (3 bases × 6)"
    );
    let candidates = candidate_set();

    let rows: Vec<SampleRow> = candidates
        .iter()
        .map(|(label, cat, v)| compute_row(columns, label, *cat, v))
        .collect();

    // Partition by regime.
    let far_rows: Vec<&SampleRow> = rows
        .iter()
        .filter(|r| r.category == SampleCategory::FarControl)
        .collect();
    let far_pairs: Vec<(usize, Option<usize>)> =
        far_rows.iter().map(|r| r.invariant_pair()).collect();
    let flat_rows: Vec<&SampleRow> = rows
        .iter()
        .filter(|r| r.category == SampleCategory::FlatTorus)
        .collect();
    let flat_pairs: Vec<(usize, Option<usize>)> =
        flat_rows.iter().map(|r| r.invariant_pair()).collect();

    // === Gate A (sampled link) ===
    // The bypass needs I to TRACK the scalar no-go: I must degenerate as the curvature mass
    // shrinks toward 0 (a would-be 4th MU vector). We test two things, both decided on EXACT
    // data (exact algebraic sign via cmp_exact_real, R04).
    //
    // (A1) EXACT falsification: if two samples have EQUAL exact curvature mass but DIFFERENT
    //      invariant pairs, then (rank_j, h1_dim) is not even a function of the scalar mass
    //      => it cannot be tracking it.
    let mut collision: Option<(
        String,
        String,
        (usize, Option<usize>),
        (usize, Option<usize>),
    )> = None;
    'scan: for i in 0..rows.len() {
        for j in (i + 1)..rows.len() {
            if rows[i].omega_mass_exact == rows[j].omega_mass_exact
                && rows[i].invariant_pair() != rows[j].invariant_pair()
            {
                collision = Some((
                    rows[i].label.clone(),
                    rows[j].label.clone(),
                    rows[i].invariant_pair(),
                    rows[j].invariant_pair(),
                ));
                break 'scan;
            }
        }
    }
    // (A2) Near-MU degeneration: order flat samples by curvature mass (exact ordering, R04) and
    //      take the most-MU-like third; do their EXACT integer invariants differ from the far
    //      controls' pair? If they are identical, flatness/MU-proximity does not move I.
    let mut flat_by_mass: Vec<&SampleRow> = flat_rows.clone();
    flat_by_mass.sort_by(|a, b| cmp_exact_real(&a.omega_mass_exact, &b.omega_mass_exact));
    let near_mu_count = (flat_by_mass.len() / 3).max(1);
    let near_mu: Vec<&SampleRow> = flat_by_mass.iter().take(near_mu_count).copied().collect();
    let near_mu_pairs: Vec<(usize, Option<usize>)> =
        near_mu.iter().map(|r| r.invariant_pair()).collect();
    let near_mu_differs_from_far = near_mu_pairs.iter().any(|p| !far_pairs.contains(p));

    // Gate A passes ONLY if the invariant is a function of the scalar (no exact collision)
    // AND the near-MU samples degenerate away from the far-control pair.
    let gate_a_pass = collision.is_none() && near_mu_differs_from_far;
    let gate_a_reason = if let Some((li, lj, pi, pj)) = &collision {
        format!(
            "EXACT decoupling: '{}' and '{}' have IDENTICAL exact curvature mass yet different \
             (rank_j, h1_dim) = {:?} vs {:?}; and the most-MU-like flat samples {:?} keep the \
             far-control pair {:?} {} => \
             sampled (rank_j, h1_dim) does not factor through scalar curvature mass on this population => Gate A FAIL",
            li,
            lj,
            pi,
            pj,
            near_mu.iter().map(|r| r.label.as_str()).collect::<Vec<_>>(),
            far_pairs.first().copied().unwrap_or((0, None)),
            // fixture: this branch does not check H^1 on the near-MU samples.
            fixtures().text("gate_a_collision_h1_note"),
        )
    } else if !near_mu_differs_from_far {
        format!(
            "the most-MU-like flat samples {:?} carry the same (rank_j, h1_dim) as the far \
             controls {:?} => flatness/MU-proximity does not move the invariant => Gate A FAIL",
            near_mu.iter().map(|r| r.label.as_str()).collect::<Vec<_>>(),
            far_pairs.first().copied().unwrap_or((0, None)),
        )
    } else {
        "near-MU flat samples degenerate away from the far-control invariant and no exact \
         mass-collision decouples it => Gate A signal"
            .to_string()
    };

    // Gate B: modal pair across the flat samples; wall = flat samples off the mode.
    let modal_pair = modal(&flat_pairs);
    let wall_samples: Vec<String> = flat_rows
        .iter()
        .filter(|r| Some(r.invariant_pair()) != modal_pair)
        .map(|r| r.label.clone())
        .collect();
    let gate_b_pass = wall_samples.is_empty();
    let gate_b_reason = if gate_b_pass {
        format!(
            "(rank_j, h1_dim) is constant = {:?} across all {} flat 5-torus samples => \
             rigid, no vector-level wall-crossing observed",
            modal_pair.unwrap_or((0, None)),
            flat_pairs.len()
        )
    } else {
        format!(
            "(rank_j, h1_dim) jumps off the modal value {:?} at {} flat sample(s) {:?} => \
             vector-level wall locus W is non-empty",
            modal_pair.unwrap_or((0, None)),
            wall_samples.len(),
            wall_samples
        )
    };

    ProbeReport {
        rows,
        gate_a_pass,
        gate_a_reason,
        gate_b_pass,
        gate_b_reason,
        wall_samples,
        terminal: "OpenResidual",
    }
}

/// The most-frequent pair (mode) of a slice; `None` if empty.
fn modal(pairs: &[(usize, Option<usize>)]) -> Option<(usize, Option<usize>)> {
    let mut best: Option<((usize, Option<usize>), usize)> = None;
    for &p in pairs {
        let count = pairs.iter().filter(|&&q| q == p).count();
        match best {
            Some((_, bc)) if bc >= count => {}
            _ => best = Some((p, count)),
        }
    }
    best.map(|(p, _)| p)
}

/// Format an optional exact rational for the table.
fn fmt_rat(r: &Option<BigRational>) -> String {
    match r {
        Some(q) => format!("{}", q),
        None => "non-rational-cyclotomic".to_string(),
    }
}

/// Render the full probe table as a printable string (reporting only).
pub fn render_table(report: &ProbeReport) -> String {
    let mut s = String::new();
    s.push_str(
        "=== MUB(6) Phase-0 exact deformation-invariance probe (vector-level, triple T0) ===\n",
    );
    s.push_str(&format!(
        "{:<14} {:<10} {:<5} {:<22} {:<12} {:<24} {:<12} {:>6} {:>6} {:>4} {:>4} {:>6} {:>6}\n",
        "label",
        "category",
        "unit",
        "f (exact)",
        "f (~f64)",
        "omega_mass (exact)",
        "mass (~f64)",
        "rankJ",
        "coker",
        "H1",
        "H2",
        "phase",
        "bianchi",
    ));
    for r in &report.rows {
        let cat = match r.category {
            SampleCategory::FarControl => "far",
            SampleCategory::FlatTorus => "flat",
        };
        let h1_str = match r.h1_dim {
            Some(h) => format!("{h}"),
            None => "N/A".to_string(),
        };
        s.push_str(&format!(
            "{:<14} {:<10} {:<5} {:<22} {:<12.6} {:<24} {:<12.6} {:>6} {:>6} {:>4} {:>4} {:>6} {:>6}\n",
            r.label,
            cat,
            r.is_unit,
            fmt_rat(&r.f_rational),
            r.f_float,
            fmt_rat(&r.omega_mass_rational),
            r.omega_mass_float,
            r.rank_j,
            r.coker_dim,
            h1_str,
            r.h2_dim,
            r.phase_gauge_in_kernel,
            r.d1_after_d0_zero,
        ));
    }
    s.push_str("\n--- Gate verdicts ---\n");
    s.push_str(&format!(
        "Gate A (no-go link): {}\n  reason: {}\n",
        if report.gate_a_pass { "SIGNAL" } else { "FAIL" },
        report.gate_a_reason
    ));
    s.push_str(&format!(
        "Gate B (rigidity):   {}\n  reason: {}\n",
        if report.gate_b_pass { "RIGID" } else { "WALL" },
        report.gate_b_reason
    ));
    s.push_str(&format!("terminal: {}\n", report.terminal));
    s
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Print the full exact table and the gate verdicts. Run with:
    /// `cargo test -j 1 -p omega_mub print_probe_table -- --nocapture`.
    #[test]
    fn print_probe_table() {
        let report = run_probe();
        println!("{}", render_table(&report));
    }

    /// Every candidate must be an exact unit vector (norm_sq == 1) by construction.
    #[test]
    fn every_candidate_is_an_exact_unit_vector() {
        let report = run_probe();
        for r in &report.rows {
            assert!(
                r.is_unit,
                "candidate {} is not an exact unit vector",
                r.label
            );
        }
    }

    /// Structural invariants that must hold at every candidate: the phase gauge lies in
    /// ker(J) and the linearized Bianchi identity d1.d0 = 0 holds exactly.
    #[test]
    fn structural_invariants_hold_everywhere() {
        let report = run_probe();
        for r in &report.rows {
            assert!(
                r.phase_gauge_in_kernel,
                "phase gauge not in ker(J) at {}",
                r.label
            );
            assert!(
                r.d1_after_d0_zero,
                "Bianchi d1.d0 = 0 failed at {}",
                r.label
            );
            // Book-keeping identities of the cochain: coker = 18 - rank_j, and with
            // rank(d1) = 2 the cohomology gives h1 = 16 - rank_j = coker - 2.
            assert_eq!(
                r.rank_j + r.coker_dim,
                super::super::d6_exact_curvature_cochain::COLUMN_COUNT
            );
            assert_eq!(r.h1_dim.map(|h| h + 2), Some(r.coker_dim));
        }
    }

    /// The flat root-of-unity candidates all sit on the 1/6-modulus torus, so each
    /// coordinate has |v_k|^2 = 1/6 exactly (a construction sanity check).
    #[test]
    fn flat_candidates_have_exact_sixth_modulus() {
        use crate::omega_native::exact::d6_exact_curvature_cochain::D;
        let target = super::rat(1, 6);
        for (_name, cat, v) in super::candidate_set() {
            if cat != SampleCategory::FlatTorus {
                continue;
            }
            for k in 0..D {
                assert_eq!(abs_sq(&v[k]), target, "flat coord modulus must be 1/6");
            }
        }
    }

    /// Terminal is OpenResidual — Phase 0 mints no authority.
    #[test]
    fn terminal_is_open_residual() {
        assert_eq!(run_probe().terminal, "OpenResidual");
    }

    // --- Observed-reality assertions (written AFTER running print_probe_table). ---
    // These pin the OBSERVED numbers so the verdict is replayable. They record the reality
    // the exact arithmetic produced on the first real --nocapture run, not a pre-supposed
    // expectation; if the computation ever changes they must be re-derived from a fresh table.

    #[test]
    fn observed_gate_verdicts_are_stable() {
        let report = run_probe();
        // OBSERVED: Gate A FAIL, Gate B WALL (not fully rigid).
        assert!(
            !report.gate_a_pass,
            "OBSERVED: Gate A must FAIL (invariant blind to no-go)"
        );
        assert!(
            !report.gate_b_pass,
            "OBSERVED: Gate B has a wall (not fully rigid)"
        );
    }

    #[test]
    fn observed_invariant_distribution() {
        let report = run_probe();
        // OBSERVED far controls: both e_0 and generic_unit are (rank_j, h1) = (11, 5).
        for r in report
            .rows
            .iter()
            .filter(|r| r.category == SampleCategory::FarControl)
        {
            assert_eq!(
                r.invariant_pair(),
                (11, Some(5)),
                "far control {} moved",
                r.label
            );
        }
        // OBSERVED: H^1 never vanishes (>= 5 everywhere) and the modal flat pair is (11, 5),
        // so the invariant cannot certify emptiness by degenerating.
        assert!(report.rows.iter().all(|r| r.h1_dim.is_some_and(|h| h >= 5)));
        // OBSERVED wall: exactly two flat samples drop to (rank_j, h1) = (10, 6).
        let mut wall = report.wall_samples.clone();
        wall.sort();
        assert_eq!(
            wall,
            vec!["flat_ramp2".to_string(), "flat_step6".to_string()]
        );
        for r in report.rows.iter().filter(|r| wall.contains(&r.label)) {
            assert_eq!(
                r.invariant_pair(),
                (10, Some(6)),
                "wall sample {} not (10,6)",
                r.label
            );
        }
    }

    #[test]
    fn observed_exact_mass_collision_decouples_invariant() {
        // OBSERVED (fully exact): generic_unit and flat_ramp2 share the exact curvature mass
        // 1/2 yet have different invariant pairs (11,5) vs (10,6) — the decisive falsification
        // that (rank_j, h1_dim) is not a function of the scalar no-go.
        let report = run_probe();
        let g = report
            .rows
            .iter()
            .find(|r| r.label == "generic_unit")
            .unwrap();
        let f = report
            .rows
            .iter()
            .find(|r| r.label == "flat_ramp2")
            .unwrap();
        assert_eq!(
            g.omega_mass_exact, f.omega_mass_exact,
            "exact masses must coincide"
        );
        assert_ne!(
            g.invariant_pair(),
            f.invariant_pair(),
            "yet invariants must differ"
        );
    }
}
