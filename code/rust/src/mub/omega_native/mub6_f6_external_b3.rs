//! MUB(6) moduli atlas — PIECE 1 gate: external `B3` candidates for `{I, F6(x,y)}`.
//!
//! The affine Fourier chart (`mub6_f6_chart`) is an exact CHM family and therefore an MU *pair*
//! chart `{I, F6(x,y)}`. No two distinct members of the family are mutually unbiased, so **no MU
//! triple lives inside the family**. Before `mub6_basis_cover` can run over an `(x,y)` box, a third
//! basis `B3` that is mutually unbiased to both `I` and `F6(x,y)` must come from **outside** the
//! family — or the locus must be certified empty.
//!
//! This module is the finite external-`B3` corpus named by the frontier status document:
//! exact-`Cyc24` candidates (product family, swapped qutrit⊗qubit products, row-dephased /
//! chirp-Fourier Butson samples) checked by exact squared-overlap arithmetic. It does **not**
//!
//! ## Locked exact findings
//!
//! * `F6(0,0)` and `F6(8,16)` are **ray-equivalent** to product `X2⊗Q0` (T0's second basis): all
//!   six column rays match. Hits with `Y2⊗Q{1,2}` are therefore **product-T0 rediscoveries**, not
//!   a new F6 moduli street.
//! * Deformed samples (e.g. `(3,7)`, `(5,13)`) share only the three D-independent left-block rays
//!   with `X2⊗Q0` and are **not** MU to the product corpus.
//! * Extended corpus (swapped product + chirp/row-dephased Butson) is checked on the deformed
//!   grid separately; see `run_extended_deformed_external_b3_gate` and the residual artifact.
//! * **Left/right split:** full MU = left-triad MU ∧ right-triad MU. Product `Y2⊗Q{1,2}` on
//!   deformed F6 is a *right-block-only* obstruction (`left_triad_mu = true`, first failure on
//!   column `i ≥ 3`). See `product_y2_deformed_right_block_obstruction_report`.
//! * **Base-MU class:** in the extended finite corpus, only `{Y2⊗Q1, Y2⊗Q2}` are fully MU to
//!   `F6(0,0)`.
//! * **Genuine Dita seeds (locked, ζ₂₄ lattice-complete for base-MU class):**
//!   Y2⊗Q1 orbit: `(0,8),(8,0),(16,16)`; Y2⊗Q2 dual orbit: `(0,16),(8,8),(16,0)`.
//!   Full 24×24 census: these are the **only** genuine-new phases (not product-ray) for each
//!   candidate. Point/neighborhood full-torus covers currently farmed for the Y2⊗Q1 orbit.
//!
//! Status contract:
//! * a *genuine-new* hit (projectively distinct from product B2) opens a cover-patch seed;
//! * T0 rediscovery must not be promoted to a new atlas street;
//! * a complete miss on a corpus is a *corpus residual*, not a no-go proof.

use serde::Serialize;

use crate::omega_native::exact::d6_exact_curvature_cochain::{
    abs_sq, inner, inv_sqrt3, omega3_pow, qubit_x, qubit_y, qutrit_q, tensor, zero_vec, ExactVec,
    D,
};
use crate::omega_native::exact::mub6_field::inv_sqrt6;
use crate::omega_native::exact::mub6_f6_chart::{f6_family_columns, f6_point_is_exact_chm};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

/// Target squared overlap for mutual unbiasedness in dimension 6.
fn target_one_over_d() -> Cyc24 {
    Cyc24::rat(ri(1) / ri(D as i64))
}

/// Exact columns of the qubit⊗qutrit product basis `X2 ⊗ Q_a` (a known CHM family member).
pub fn product_x2_qa_columns(a: i64) -> [ExactVec; D] {
    let x2 = qubit_x();
    let qa = qutrit_q(a);
    let mut cols: [ExactVec; D] = std::array::from_fn(|_| zero_vec());
    let mut idx = 0;
    for qb in &x2 {
        for qt in &qa {
            cols[idx] = tensor(qb, qt);
            idx += 1;
        }
    }
    cols
}

/// Exact columns of the qubit⊗qutrit product basis `Y2 ⊗ Q_a`.
pub fn product_y2_qa_columns(a: i64) -> [ExactVec; D] {
    let y2 = qubit_y();
    let qa = qutrit_q(a);
    let mut cols: [ExactVec; D] = std::array::from_fn(|_| zero_vec());
    let mut idx = 0;
    for qb in &y2 {
        for qt in &qa {
            cols[idx] = tensor(qb, qt);
            idx += 1;
        }
    }
    cols
}

/// Tensor for the **swapped** identification `ℂ⁶ ≅ ℂ³ ⊗ ℂ²` (qutrit outer, qubit inner).
fn tensor_qutrit_qubit(qt: &[Cyc24; 3], qb: &[Cyc24; 2]) -> ExactVec {
    let mut out = zero_vec();
    for (a, qa) in qt.iter().enumerate() {
        for (b, qbt) in qb.iter().enumerate() {
            out[a * 2 + b] = qa.mul(qbt);
        }
    }
    out
}

fn qutrit_f3() -> [[Cyc24; 3]; 3] {
    let s = inv_sqrt3();
    std::array::from_fn(|m| std::array::from_fn(|j| omega3_pow((j * m) as i64).mul(&s)))
}

/// Exact columns of the swapped product `Q_a ⊗ X2` (CHM under `ℂ³ ⊗ ℂ²`).
pub fn product_qa_x2_columns(a: i64) -> [ExactVec; D] {
    let qa = qutrit_q(a);
    let x2 = qubit_x();
    let mut cols: [ExactVec; D] = std::array::from_fn(|_| zero_vec());
    let mut idx = 0;
    for qt in &qa {
        for qb in &x2 {
            cols[idx] = tensor_qutrit_qubit(qt, qb);
            idx += 1;
        }
    }
    cols
}

/// Exact columns of the swapped product `Q_a ⊗ Y2`.
pub fn product_qa_y2_columns(a: i64) -> [ExactVec; D] {
    let qa = qutrit_q(a);
    let y2 = qubit_y();
    let mut cols: [ExactVec; D] = std::array::from_fn(|_| zero_vec());
    let mut idx = 0;
    for qt in &qa {
        for qb in &y2 {
            cols[idx] = tensor_qutrit_qubit(qt, qb);
            idx += 1;
        }
    }
    cols
}

/// Exact columns of the swapped product `F3 ⊗ X2`.
pub fn product_f3_x2_columns() -> [ExactVec; D] {
    let f3 = qutrit_f3();
    let x2 = qubit_x();
    let mut cols: [ExactVec; D] = std::array::from_fn(|_| zero_vec());
    let mut idx = 0;
    for qt in &f3 {
        for qb in &x2 {
            cols[idx] = tensor_qutrit_qubit(qt, qb);
            idx += 1;
        }
    }
    cols
}

/// Exact columns of the swapped product `F3 ⊗ Y2`.
pub fn product_f3_y2_columns() -> [ExactVec; D] {
    let f3 = qutrit_f3();
    let y2 = qubit_y();
    let mut cols: [ExactVec; D] = std::array::from_fn(|_| zero_vec());
    let mut idx = 0;
    for qt in &f3 {
        for qb in &y2 {
            cols[idx] = tensor_qutrit_qubit(qt, qb);
            idx += 1;
        }
    }
    cols
}

/// Order-6 Fourier / chirp-Butson matrix over `Q(ζ₂₄)`:
/// `H_{jk} = ζ₆^{j k + α j²} / √6` with `ζ₆ = ζ₂₄⁴`.
///
/// Row quadratic phases preserve the CHM property of the DFT (row dephasing of a CHM is a CHM).
pub fn chirp_fourier6_columns(alpha: i64) -> [ExactVec; D] {
    let s = inv_sqrt6();
    std::array::from_fn(|k| {
        std::array::from_fn(|j| {
            // ζ₆^{j k + α j²} = ζ₂₄^{4(jk + α j²)}
            let exp =
                (4 * ((j as i64) * (k as i64) + alpha * (j as i64) * (j as i64))).rem_euclid(24);
            Cyc24::zeta24(exp as i32).mul(&s)
        })
    })
}

/// Row-dephase an existing CHM: multiply row `r` by `ζ₂₄^{phases[r]}`. Preserves the CHM property.
pub fn row_dephase_columns(cols: &[ExactVec; D], phases: [i32; D]) -> [ExactVec; D] {
    std::array::from_fn(|c| std::array::from_fn(|r| cols[c][r].mul(&Cyc24::zeta24(phases[r]))))
}

/// Exact: every entry of every column has modulus² = 1/6 (CHM / MU-to-standard).
pub fn basis_is_exact_chm(cols: &[ExactVec; D]) -> bool {
    let target = target_one_over_d();
    let one = Cyc24::rat(ri(1));
    let zero = Cyc24::zero();
    for col in cols {
        for entry in col {
            if abs_sq(entry) != target {
                return false;
            }
        }
    }
    for i in 0..D {
        for j in 0..D {
            let ip = inner(&cols[i], &cols[j]);
            let want = if i == j { &one } else { &zero };
            if &ip != want {
                return false;
            }
        }
    }
    true
}

/// Exact mutual unbiasedness of two orthonormal bases: `|⟨A_i, B_j⟩|² = 1/6` for all `i, j`.
pub fn bases_are_mutually_unbiased(a: &[ExactVec; D], b: &[ExactVec; D]) -> bool {
    let target = target_one_over_d();
    for i in 0..D {
        for j in 0..D {
            if abs_sq(&inner(&a[i], &b[j])) != target {
                return false;
            }
        }
    }
    true
}

/// One external-`B3` candidate: identity, construction recipe, and exact columns.
#[derive(Debug, Clone)]
pub struct ExternalB3Candidate {
    pub id: &'static str,
    pub family: &'static str,
    pub columns: [ExactVec; D],
}

/// Finite first corpus: product-family CHMs outside the affine Fourier (Dita) chart.
///
/// These are the standard qubit⊗qutrit MUB factors that already participate in the canonical
/// triple `T0 = {I, X2⊗Q0, Y2⊗Q1}`. They are *not* members of the Dita `F6(x,y)` family (different
/// block structure), so they are legitimate external-`B3` probes for the F6 gate.
pub fn external_b3_product_corpus() -> Vec<ExternalB3Candidate> {
    let mut out = Vec::with_capacity(6);
    for a in 0..3 {
        out.push(ExternalB3Candidate {
            id: match a {
                0 => "X2_tensor_Q0",
                1 => "X2_tensor_Q1",
                _ => "X2_tensor_Q2",
            },
            family: "qubit_x_tensor_qutrit_quadratic_gauss",
            columns: product_x2_qa_columns(a),
        });
        out.push(ExternalB3Candidate {
            id: match a {
                0 => "Y2_tensor_Q0",
                1 => "Y2_tensor_Q1",
                _ => "Y2_tensor_Q2",
            },
            family: "qubit_y_tensor_qutrit_quadratic_gauss",
            columns: product_y2_qa_columns(a),
        });
    }
    out
}

/// Swapped product corpus under `ℂ⁶ ≅ ℂ³ ⊗ ℂ²` (distinct block structure from qubit⊗qutrit).
pub fn external_b3_swapped_product_corpus() -> Vec<ExternalB3Candidate> {
    let mut out = Vec::with_capacity(8);
    for a in 0..3 {
        out.push(ExternalB3Candidate {
            id: match a {
                0 => "Q0_tensor_X2",
                1 => "Q1_tensor_X2",
                _ => "Q2_tensor_X2",
            },
            family: "qutrit_quadratic_gauss_tensor_qubit_x",
            columns: product_qa_x2_columns(a),
        });
        out.push(ExternalB3Candidate {
            id: match a {
                0 => "Q0_tensor_Y2",
                1 => "Q1_tensor_Y2",
                _ => "Q2_tensor_Y2",
            },
            family: "qutrit_quadratic_gauss_tensor_qubit_y",
            columns: product_qa_y2_columns(a),
        });
    }
    out.push(ExternalB3Candidate {
        id: "F3_tensor_X2",
        family: "qutrit_fourier_tensor_qubit_x",
        columns: product_f3_x2_columns(),
    });
    out.push(ExternalB3Candidate {
        id: "F3_tensor_Y2",
        family: "qutrit_fourier_tensor_qubit_y",
        columns: product_f3_y2_columns(),
    });
    out
}

/// Exact Butson / dephased-Fourier samples outside the two product families.
///
/// Chirp DFT (`α ∈ {0,1,2,3}`) and a few row-dephasings of `F6(0,0)` and deformed `F6(3,7)`.
/// Only candidates that pass `basis_is_exact_chm` are retained (all of these constructions are
/// designed to be CHMs; the filter is the safety net).
pub fn external_b3_butson_corpus() -> Vec<ExternalB3Candidate> {
    let mut out = Vec::new();
    for alpha in 0..4 {
        let cols = chirp_fourier6_columns(alpha);
        if basis_is_exact_chm(&cols) {
            out.push(ExternalB3Candidate {
                id: match alpha {
                    0 => "chirp_fourier6_a0",
                    1 => "chirp_fourier6_a1",
                    2 => "chirp_fourier6_a2",
                    _ => "chirp_fourier6_a3",
                },
                family: "order6_chirp_fourier_butson",
                columns: cols,
            });
        }
    }
    let base = f6_family_columns(0, 0);
    let deformed = f6_family_columns(3, 7);
    let phase_patterns: [([i32; D], &'static str); 4] = [
        ([0, 4, 8, 12, 16, 20], "row_dephase_F6_00_sixth"),
        ([0, 6, 12, 18, 0, 6], "row_dephase_F6_00_fourth"),
        ([0, 3, 6, 9, 12, 15], "row_dephase_F6_00_eighth"),
        ([0, 4, 8, 12, 16, 20], "row_dephase_F6_37_sixth"),
    ];
    for (i, (phases, id)) in phase_patterns.iter().enumerate() {
        let src = if i < 3 { &base } else { &deformed };
        let cols = row_dephase_columns(src, *phases);
        if basis_is_exact_chm(&cols) {
            out.push(ExternalB3Candidate {
                id,
                family: "row_dephased_f6_butson",
                columns: cols,
            });
        }
    }
    out
}

/// Extended finite corpus: product ∪ swapped-product ∪ Butson/dephased samples.
pub fn external_b3_extended_corpus() -> Vec<ExternalB3Candidate> {
    let mut out = external_b3_product_corpus();
    out.extend(external_b3_swapped_product_corpus());
    out.extend(external_b3_butson_corpus());
    out
}

/// Exact count of column rays shared by two orthonormal bases: number of pairs `(i,j)` with
/// `|⟨A_i, B_j⟩|² = 1` (same complex line). Equal to `D` iff the bases are the same up to column
/// phase and permutation (projective ray equivalence).
pub fn column_ray_match_count(a: &[ExactVec; D], b: &[ExactVec; D]) -> usize {
    let one = Cyc24::rat(ri(1));
    let mut n = 0usize;
    for i in 0..D {
        for j in 0..D {
            if abs_sq(&inner(&a[i], &b[j])) == one {
                n += 1;
            }
        }
    }
    n
}

/// `true` iff `a` and `b` determine the same unordered set of projective column rays.
pub fn bases_are_ray_equivalent(a: &[ExactVec; D], b: &[ExactVec; D]) -> bool {
    column_ray_match_count(a, b) == D
}

/// Classification of an MU hit relative to the known product triple `T0 = {I, X2⊗Q0, Y2⊗Q1}`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum ExternalB3HitClass {
    /// `F6(dx,dy)` is ray-equivalent to product `X2⊗Q0` (T0's second basis). The hit rediscovers
    /// the product triple already covered by the fixed-tuple / T0 neighborhood program — **not** a
    /// new F6-chart street of the moduli.
    ProductT0Rediscovery,
    /// `F6(dx,dy)` is projectively distinct from `X2⊗Q0` and still admits this external B3. A
    /// genuine new chart seed for a cover patch.
    GenuineNewF6Seed,
}

/// One exact evaluation of a candidate against a fixed F6 chart point.
#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct ExternalB3Hit {
    pub f6_dx: i64,
    pub f6_dy: i64,
    pub candidate_id: String,
    pub candidate_is_chm: bool,
    pub mu_to_f6: bool,
    /// Ray-match count of `F6(dx,dy)` against product `X2⊗Q0` (diagnostic for rediscovery).
    pub f6_ray_matches_product_x2q0: usize,
    pub class: ExternalB3HitClass,
}

/// Gate terminal for the external-`B3` search on a declared finite corpus + F6 parameter grid.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum ExternalB3GateTerminal {
    /// At least one **projectively new** exact MU triple seed on the F6 chart (not ray-equivalent
    /// to the product `T0` second basis).
    GenuineNewSeedFound,
    /// Hits exist, but every hit is a product-`T0` rediscovery (`F6` ray-equivalent to `X2⊗Q0`).
    /// PIECE 1 remains gated for deformed F6 points; no new cover street opens.
    OnlyProductT0Rediscovery,
    /// Corpus exhausted on the declared grid with zero MU hits. This is **not** a no-go: only the
    /// searched finite set is ruled out.
    CorpusExhaustedOpenResidual,
}

/// Structured report of the external-`B3` gate run.
#[derive(Debug, Clone, Serialize)]
pub struct ExternalB3GateReport {
    pub chart_id: &'static str,
    pub corpus_size: usize,
    pub f6_grid_size: usize,
    pub evaluations: usize,
    pub hits: Vec<ExternalB3Hit>,
    pub genuine_new_seed_count: usize,
    pub t0_rediscovery_count: usize,
    pub terminal: ExternalB3GateTerminal,
    pub open_obligation: &'static str,
    pub firewall: &'static str,
}

/// Discrete root-of-unity F6 parameter sample used as the first search grid.
///
/// Includes:
/// * base-ray class points `(0,0)`, `(8,16)`, `(16,8)` (T0 rediscovery locus for product B3);
/// * **genuine Dita seeds** `(0,8)`, `(8,0)`, `(16,16)` where `Y2⊗Q1` is MU to a projectively
///   deformed F6 (ray-match count 3 against product `X2⊗Q0`);
/// * generic deformed probes that remain non-MU to the product corpus.
pub fn default_f6_probe_grid() -> Vec<(i64, i64)> {
    vec![
        (0, 0),
        (8, 16),
        (16, 8),
        // Genuine-new seeds for Y2⊗Q1 (locked by phase-stabilizer census):
        (0, 8),
        (8, 0),
        (16, 16),
        // Generic deformed non-seeds:
        (3, 7),
        (11, 23),
        (5, 13),
        (1, 1),
        (4, 12),
        (6, 18),
    ]
}

/// Locked exact genuine-new Dita triple seeds: `{I, F6(dx,dy), Y2⊗Q1}` with `F6` **not**
/// ray-equivalent to product `X2⊗Q0`.
///
/// These open a real PIECE-1 cover street (fixed-triple seeds). They do **not** alone prove
/// `MUB(6)=3` and mint no authority.
pub fn genuine_dita_y2q1_triple_seeds() -> Vec<(i64, i64)> {
    vec![(0, 8), (8, 0), (16, 16)]
}

/// Locked exact genuine-new Dita triple seeds for external B3 = `Y2⊗Q2`:
/// `{I, F6(dx,dy), Y2⊗Q2}` with F6 not ray-equivalent to product `X2⊗Q0`.
///
/// Discrete ζ₂₄ lattice dual to the Y2⊗Q1 orbit (locked by full 24×24 census 2026-07-24r).
pub fn genuine_dita_y2q2_triple_seeds() -> Vec<(i64, i64)> {
    vec![(0, 16), (8, 8), (16, 0)]
}

/// Run the exact external-`B3` gate: for each `(dx,dy)` and each corpus candidate, decide whether
/// `{I, F6(dx,dy), candidate}` is an exact MU triple (candidate CHM ∧ MU to F6).
///
/// Hits are classified against product `X2⊗Q0` so that rediscoveries of the canonical product
/// triple are not promoted to a new F6 moduli street.
///
/// Preconditions checked exactly: every probed F6 point must itself be a CHM (`f6_point_is_exact_chm`).
pub fn run_external_b3_gate(
    f6_grid: &[(i64, i64)],
    corpus: &[ExternalB3Candidate],
) -> ExternalB3GateReport {
    let product_x2q0 = product_x2_qa_columns(0);
    let mut hits = Vec::new();
    let mut evaluations = 0usize;

    for &(dx, dy) in f6_grid {
        assert!(
            f6_point_is_exact_chm(dx, dy),
            "F6({dx},{dy}) must be an exact CHM before the B3 gate runs"
        );
        let f6 = f6_family_columns(dx, dy);
        let ray_matches = column_ray_match_count(&f6, &product_x2q0);
        let f6_is_product_b2 = ray_matches == D;
        for cand in corpus {
            evaluations += 1;
            let is_chm = basis_is_exact_chm(&cand.columns);
            let mu = is_chm && bases_are_mutually_unbiased(&f6, &cand.columns);
            if mu {
                let class = if f6_is_product_b2 {
                    ExternalB3HitClass::ProductT0Rediscovery
                } else {
                    ExternalB3HitClass::GenuineNewF6Seed
                };
                hits.push(ExternalB3Hit {
                    f6_dx: dx,
                    f6_dy: dy,
                    candidate_id: cand.id.to_string(),
                    candidate_is_chm: true,
                    mu_to_f6: true,
                    f6_ray_matches_product_x2q0: ray_matches,
                    class,
                });
            }
        }
    }

    let genuine_new_seed_count = hits
        .iter()
        .filter(|h| h.class == ExternalB3HitClass::GenuineNewF6Seed)
        .count();
    let t0_rediscovery_count = hits
        .iter()
        .filter(|h| h.class == ExternalB3HitClass::ProductT0Rediscovery)
        .count();

    let terminal = if genuine_new_seed_count > 0 {
        ExternalB3GateTerminal::GenuineNewSeedFound
    } else if t0_rediscovery_count > 0 {
        ExternalB3GateTerminal::OnlyProductT0Rediscovery
    } else {
        ExternalB3GateTerminal::CorpusExhaustedOpenResidual
    };

    ExternalB3GateReport {
        chart_id: "mub6-moduli-piece1-affine-fourier-F6",
        corpus_size: corpus.len(),
        f6_grid_size: f6_grid.len(),
        evaluations,
        hits,
        genuine_new_seed_count,
        t0_rediscovery_count,
        terminal,
        open_obligation: "for deformed F6(x,y) (ray-distinct from X2⊗Q0) either exhibit a genuine-new external B3 seed and run mub6_basis_cover, or certify emptiness on that locus; finite Cyc24 corpus is non-exhaustive; T0 rediscovery is not a new atlas street",
        firewall: "finite exact Cyc24 corpus only; T0 rediscovery is not a new atlas street; miss is OpenResidual not no-go; stated region only; mints no authority",
    }
}

/// Convenience: product corpus on the default F6 probe grid.
pub fn run_default_external_b3_gate() -> ExternalB3GateReport {
    let corpus = external_b3_product_corpus();
    run_external_b3_gate(&default_f6_probe_grid(), &corpus)
}

/// **Structural fact (exact):** the three *left* columns of `F6(dx,dy)` are independent of
/// `(dx,dy)` (Dita `D` only multiplies the right block). Consequently they are always
/// ray-equivalent to the three left columns of `F6(0,0)`.
///
/// This is the load-bearing obstruction seed for emptiness arguments on the deformed chart:
/// any external B3 that is MU to a deformed `F6` must still be MU to this fixed left triad,
/// which is shared with the product base point.
pub fn f6_left_block_independent_of_phases(dx: i64, dy: i64) -> bool {
    let a = f6_family_columns(dx, dy);
    let b = f6_family_columns(0, 0);
    let one = Cyc24::rat(ri(1));
    // Left columns 0..3: each of `a`'s left columns matches some left column of `b` as a ray.
    for i in 0..3 {
        let mut matched = false;
        for j in 0..3 {
            if abs_sq(&inner(&a[i], &b[j])) == one {
                matched = true;
                break;
            }
        }
        if !matched {
            return false;
        }
    }
    true
}

/// Exact: `|⟨f6_col_i, b3_col_j⟩|² = 1/6` for every left-block column `i ∈ {0,1,2}` and all `j`.
pub fn is_mu_to_f6_left_triad(f6: &[ExactVec; D], b3: &[ExactVec; D]) -> bool {
    let target = target_one_over_d();
    for i in 0..3 {
        for j in 0..D {
            if abs_sq(&inner(&f6[i], &b3[j])) != target {
                return false;
            }
        }
    }
    true
}

/// Exact: same for the right-block columns `i ∈ {3,4,5}`.
pub fn is_mu_to_f6_right_triad(f6: &[ExactVec; D], b3: &[ExactVec; D]) -> bool {
    let target = target_one_over_d();
    for i in 3..D {
        for j in 0..D {
            if abs_sq(&inner(&f6[i], &b3[j])) != target {
                return false;
            }
        }
    }
    true
}

/// First exact MU-failure witness `(f6_col, b3_col)` with `|⟨·,·⟩|² ≠ 1/6`, if any.
pub fn first_mu_failure(f6: &[ExactVec; D], b3: &[ExactVec; D]) -> Option<(usize, usize)> {
    let target = target_one_over_d();
    for i in 0..D {
        for j in 0..D {
            if abs_sq(&inner(&f6[i], &b3[j])) != target {
                return Some((i, j));
            }
        }
    }
    None
}

/// **Necessity lemma (exact arithmetic check form).**
///
/// If `B3` is mutually unbiased to `F6(dx,dy)`, then it is mutually unbiased to the **base**
/// left triad of `F6(0,0)` (because left columns of every F6 point are ray-equivalent to those
/// of `F6(0,0)`, and ray-equivalent unit vectors share all squared overlaps with any third
/// vector up to a unimodular phase that cancels in `|·|²`).
///
/// Implemented as the contrapositive-ready predicate:
/// `full_mu ⇒ left_mu_to_base`, checked by direct evaluation on supplied columns.
pub fn mu_to_f6_implies_mu_to_base_left_triad(dx: i64, dy: i64, b3: &[ExactVec; D]) -> bool {
    let f6 = f6_family_columns(dx, dy);
    let base = f6_family_columns(0, 0);
    if !bases_are_mutually_unbiased(&f6, b3) {
        // Vacuous: the implication antecedent is false.
        return true;
    }
    is_mu_to_f6_left_triad(&base, b3)
}

/// **Deformed-chart split certificate** for a candidate `B3` against `F6(dx,dy)`:
/// records whether left-triad MU holds, whether right-triad MU holds, and the first full failure.
///
/// For product `Y2⊗Q{1,2}` against deformed F6 this yields the locked pattern
/// `left_ok = true`, `right_ok = false`, `first_failure.0 ≥ 3` — the candidate survives the
/// phase-independent left obstruction inherited from `T0` but dies on the deformed right block.
#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
pub struct DeformedF6SplitCertificate {
    pub f6_dx: i64,
    pub f6_dy: i64,
    pub candidate_id: String,
    pub left_triad_mu: bool,
    pub right_triad_mu: bool,
    pub full_mu: bool,
    pub first_failure: Option<(usize, usize)>,
    /// `true` when left holds, right fails, and the first failure is a right-block column.
    pub right_block_only_obstruction: bool,
}

/// Build the split certificate for one candidate against one F6 point.
pub fn deformed_f6_split_certificate(
    dx: i64,
    dy: i64,
    candidate_id: &str,
    b3: &[ExactVec; D],
) -> DeformedF6SplitCertificate {
    let f6 = f6_family_columns(dx, dy);
    let left_triad_mu = is_mu_to_f6_left_triad(&f6, b3);
    let right_triad_mu = is_mu_to_f6_right_triad(&f6, b3);
    let first_failure = first_mu_failure(&f6, b3);
    let full_mu = first_failure.is_none();
    let right_block_only_obstruction =
        left_triad_mu && !right_triad_mu && first_failure.map(|(i, _)| i >= 3).unwrap_or(false);
    DeformedF6SplitCertificate {
        f6_dx: dx,
        f6_dy: dy,
        candidate_id: candidate_id.to_string(),
        left_triad_mu,
        right_triad_mu,
        full_mu,
        first_failure,
        right_block_only_obstruction,
    }
}

/// Run split certificates for the product `Y2⊗Q{1,2}` bases (the T0 third-basis class) on the
/// deformed F6 probe grid. These are exactly the candidates that **pass** left-triad MU (they
/// complete `T0` at the base point) and therefore isolate the deformed right-block residual.
pub fn product_y2_deformed_right_block_obstruction_report() -> Vec<DeformedF6SplitCertificate> {
    let mut out = Vec::new();
    for a in 1..=2 {
        let cols = product_y2_qa_columns(a);
        let id = if a == 1 {
            "Y2_tensor_Q1"
        } else {
            "Y2_tensor_Q2"
        };
        for &(dx, dy) in &deformed_f6_probe_grid() {
            out.push(deformed_f6_split_certificate(dx, dy, id, &cols));
        }
    }
    out
}

/// Members of the extended finite corpus that are fully MU to the base chart point `F6(0,0)`.
///
/// These are the only corpus candidates that could possibly form an MU triple `{I, F6(0,0), B3}`
/// and therefore the only ones that can exhibit a pure right-block residual under Dita deformation
/// (they already pass left-triad MU at the base, and left columns do not move).
pub fn extended_corpus_mu_to_base_f6() -> Vec<ExternalB3Candidate> {
    let f00 = f6_family_columns(0, 0);
    external_b3_extended_corpus()
        .into_iter()
        .filter(|c| bases_are_mutually_unbiased(&f00, &c.columns))
        .collect()
}

/// **Class-wide deformed obstruction report** for every extended-corpus candidate that is fully
/// MU to `F6(0,0)`: on each deformed probe point, emit the left/right split certificate.
///
/// Locked pattern expected for this finite class: every certificate has
/// `right_block_only_obstruction = true` and `full_mu = false`. This upgrades the Y2-only
/// observation to the full base-MU subclass of the extended corpus — still a **finite class**
/// residual, not a continuous no-go for all possible external B3.
#[derive(Debug, Clone, Serialize)]
pub struct BaseMuClassDeformedObstructionReport {
    pub base_mu_class_size: usize,
    pub base_mu_candidate_ids: Vec<String>,
    pub deformed_grid_size: usize,
    pub certificates: Vec<DeformedF6SplitCertificate>,
    /// `true` iff every cert is a right-block-only obstruction (no full MU on deformed grid).
    pub all_right_block_only: bool,
    pub any_full_mu_on_deformed: bool,
    pub open_obligation: &'static str,
    pub firewall: &'static str,
}

/// Run the class-wide base-MU → deformed-right-block obstruction analysis.
pub fn base_mu_class_deformed_obstruction_report() -> BaseMuClassDeformedObstructionReport {
    let class = extended_corpus_mu_to_base_f6();
    let grid = deformed_f6_probe_grid();
    let mut certificates = Vec::new();
    for cand in &class {
        for &(dx, dy) in &grid {
            certificates.push(deformed_f6_split_certificate(
                dx,
                dy,
                cand.id,
                &cand.columns,
            ));
        }
    }
    let all_right_block_only = !certificates.is_empty()
        && certificates
            .iter()
            .all(|c| c.right_block_only_obstruction && !c.full_mu);
    let any_full_mu_on_deformed = certificates.iter().any(|c| c.full_mu);
    BaseMuClassDeformedObstructionReport {
        base_mu_class_size: class.len(),
        base_mu_candidate_ids: class.iter().map(|c| c.id.to_string()).collect(),
        deformed_grid_size: grid.len(),
        certificates,
        all_right_block_only,
        any_full_mu_on_deformed,
        open_obligation: "finite base-MU subclass of the extended corpus is right-block-obstructed on the deformed Dita probe grid; continuous emptiness for all external B3 (or a sporadic seed outside this class) remains open",
        firewall: "finite Cyc24 corpus class only; not a continuous no-go; stated region only; mints no authority",
    }
}

/// Exact residual mass of a candidate against the **right triad only** of `F6(dx,dy)`:
/// `∑_{i=3..5} ∑_j (|⟨F6_i, B3_j⟩|² − 1/6)²` as an exact `Cyc24` value (should be a non-negative
/// rational cyclotomic; compared against zero for obstruction).
pub fn right_triad_residual_mass(dx: i64, dy: i64, b3: &[ExactVec; D]) -> Cyc24 {
    let f6 = f6_family_columns(dx, dy);
    let target = target_one_over_d();
    let mut acc = Cyc24::zero();
    for i in 3..D {
        for j in 0..D {
            let dev = abs_sq(&inner(&f6[i], &b3[j])).sub(&target);
            acc = acc.add(&dev.mul(&dev));
        }
    }
    acc
}

/// `true` iff the right-triad residual mass is exactly zero (right-triad MU).
pub fn right_triad_residual_is_zero(dx: i64, dy: i64, b3: &[ExactVec; D]) -> bool {
    right_triad_residual_mass(dx, dy, b3).is_zero()
}

// ---------------------------------------------------------------------------
// Algebraic right-block dephasing (exact identity for the Dita right triad)
// ---------------------------------------------------------------------------

/// F3 entry `(j,m) = η^{jm}`, `η = ζ₂₄⁸`.
fn f3_entry(j: usize, m: usize) -> Cyc24 {
    Cyc24::zeta24(((8 * j * m) % 24) as i32)
}

/// Dita diagonal phases `D = diag(1, ζ^{dx}, ζ^{dy})`.
fn dita_phases(dx: i64, dy: i64) -> [Cyc24; 3] {
    [
        Cyc24::rat(ri(1)),
        Cyc24::zeta24(dx as i32),
        Cyc24::zeta24(dy as i32),
    ]
}

/// **Algebraic kernel** of the right-block overlap for one B3 column `w` and right-block index
/// `m ∈ {0,1,2}` (F6 column `m+3`):
///
/// ```text
///   z_j = conj(F3(j,m)/√6) · (w_j − w_{j+3}),   j ∈ {0,1,2}
///   ⟨R_m(D), w⟩ = ∑_j conj(D_j) · z_j
/// ```
///
/// with `D = diag(1, ζ^{dx}, ζ^{dy})`. This is the exact reduction used for the right-block
/// residual: left-triad MU constrains the sums `(w_j + w_{j+3})`; right-triad MU constrains the
/// dephased sums `(w_j − w_{j+3})` against `D`.
pub fn right_block_z_coeffs(m: usize, w: &ExactVec) -> [Cyc24; 3] {
    debug_assert!(m < 3);
    let s = inv_sqrt6();
    std::array::from_fn(|j| {
        let f = f3_entry(j, m).mul(&s);
        let diff = w[j].sub(&w[j + 3]);
        f.conj().mul(&diff)
    })
}

/// Exact right-block overlap `⟨R_m(D), w⟩` via the dephasing formula (not via full F6 assembly).
pub fn right_overlap_via_dephasing(dx: i64, dy: i64, m: usize, w: &ExactVec) -> Cyc24 {
    let z = right_block_z_coeffs(m, w);
    let d = dita_phases(dx, dy);
    let mut acc = Cyc24::zero();
    for j in 0..3 {
        acc = acc.add(&d[j].conj().mul(&z[j]));
    }
    acc
}

/// Direct right-block overlap from assembled `F6(dx,dy)` column `m+3` (oracle for the formula).
pub fn right_overlap_direct(dx: i64, dy: i64, m: usize, w: &ExactVec) -> Cyc24 {
    let f6 = f6_family_columns(dx, dy);
    inner(&f6[m + 3], w)
}

/// `true` iff algebraic dephasing formula matches the assembled F6 right-column inner product
/// for every right index `m` and every column of `b3`.
pub fn right_dephasing_formula_matches_assembly(dx: i64, dy: i64, b3: &[ExactVec; D]) -> bool {
    for m in 0..3 {
        for w in b3 {
            if right_overlap_via_dephasing(dx, dy, m, w) != right_overlap_direct(dx, dy, m, w) {
                return false;
            }
        }
    }
    true
}

/// Discrete **phase stabilizer** of a base-MU candidate: the set of root-of-unity `(dx,dy)` for
/// which `{I, F6(dx,dy), B3}` remains fully mutually unbiased.
///
/// For the product `Y2⊗Q{1,2}` class this is expected to coincide with the F6 points that are
/// **ray-equivalent to `F6(0,0)`** (the base chart ray), i.e. pure Dita deformation leaves the
/// triple only when it does not move the projective second basis.
#[derive(Debug, Clone, Serialize)]
pub struct BaseMuPhaseStabilizerCensus {
    pub candidate_id: String,
    pub grid_size: usize,
    pub full_mu_count: usize,
    pub full_mu_phases: Vec<(i64, i64)>,
    pub ray_equivalent_to_base_count: usize,
    /// `true` iff every full-MU phase is ray-equivalent to `F6(0,0)` / product `X2⊗Q0`.
    pub full_mu_subseteq_base_ray_class: bool,
    /// `true` iff conversely every base-ray phase on the grid is full-MU for this candidate.
    pub base_ray_class_subseteq_full_mu: bool,
    pub firewall: &'static str,
}

/// Fast right-triad MU check via the dephasing formula (no full F6 assembly).
///
/// For a **base-MU** candidate, left-triad MU holds at every phase (left block independent), so
/// full MU to `F6(dx,dy)` reduces exactly to this right-triad check.
pub fn is_mu_to_right_triad_via_dephasing(dx: i64, dy: i64, b3: &[ExactVec; D]) -> bool {
    let target = target_one_over_d();
    for m in 0..3 {
        for w in b3 {
            if abs_sq(&right_overlap_via_dephasing(dx, dy, m, w)) != target {
                return false;
            }
        }
    }
    true
}

/// Census of root-of-unity phases where a fixed **base-MU** B3 stays fully MU to `F6(dx,dy)`.
///
/// Uses the dephasing formula for the right triad (left is automatic for the base-MU class).
pub fn base_mu_phase_stabilizer_census(
    candidate_id: &str,
    b3: &[ExactVec; D],
    grid: &[(i64, i64)],
) -> BaseMuPhaseStabilizerCensus {
    let xq0 = product_x2_qa_columns(0);
    let mut full_mu_phases = Vec::new();
    let mut ray_equivalent_to_base_count = 0usize;
    for &(dx, dy) in grid {
        let f6 = f6_family_columns(dx, dy);
        let is_base_ray = bases_are_ray_equivalent(&f6, &xq0);
        if is_base_ray {
            ray_equivalent_to_base_count += 1;
        }
        // Base-MU class: full MU ⇔ right-triad MU via dephasing.
        if is_mu_to_right_triad_via_dephasing(dx, dy, b3) {
            full_mu_phases.push((dx, dy));
        }
    }
    let full_mu_subseteq_base_ray_class = full_mu_phases
        .iter()
        .all(|&(dx, dy)| bases_are_ray_equivalent(&f6_family_columns(dx, dy), &xq0));
    let base_ray_class_subseteq_full_mu = grid.iter().all(|&(dx, dy)| {
        let f6 = f6_family_columns(dx, dy);
        if bases_are_ray_equivalent(&f6, &xq0) {
            is_mu_to_right_triad_via_dephasing(dx, dy, b3)
        } else {
            true
        }
    });
    BaseMuPhaseStabilizerCensus {
        candidate_id: candidate_id.to_string(),
        grid_size: grid.len(),
        full_mu_count: full_mu_phases.len(),
        full_mu_phases,
        ray_equivalent_to_base_count,
        full_mu_subseteq_base_ray_class,
        base_ray_class_subseteq_full_mu,
        firewall: "discrete root-of-unity census only; not continuous stabilizer; stated region only; mints no authority",
    }
}

/// Coarse root-of-unity grid with step `step` in each phase (still exact ζ₂₄ samples).
pub fn root_of_unity_f6_grid_step(step: i64) -> Vec<(i64, i64)> {
    assert!(step > 0 && 24 % step == 0);
    let mut g = Vec::new();
    let mut dx = 0i64;
    while dx < 24 {
        let mut dy = 0i64;
        while dy < 24 {
            g.push((dx, dy));
            dy += step;
        }
        dx += step;
    }
    g
}

/// Partition of full-MU lattice phases for a base-MU B3 into T0-rediscovery vs genuine-new.
#[derive(Debug, Clone, Serialize)]
pub struct DiscreteF6BaseMuLatticeExhaustion {
    pub candidate_id: String,
    pub grid_size: usize,
    pub full_mu_phases: Vec<(i64, i64)>,
    pub t0_rediscovery_phases: Vec<(i64, i64)>,
    pub genuine_new_phases: Vec<(i64, i64)>,
    pub locked_genuine_seeds: Vec<(i64, i64)>,
    /// `true` iff `genuine_new_phases` equals `locked_genuine_seeds` as sets.
    pub genuine_new_equals_locked_seeds: bool,
    /// `true` iff Y2⊗Q2 (or this candidate) has no genuine-new phases on the grid.
    pub no_genuine_new: bool,
    pub firewall: &'static str,
}

/// Exhaust a root-of-unity F6 grid for one base-MU candidate, classifying each full-MU phase.
pub fn exhaust_base_mu_f6_lattice(
    candidate_id: &str,
    b3: &[ExactVec; D],
    grid: &[(i64, i64)],
    locked_genuine_seeds: &[(i64, i64)],
) -> DiscreteF6BaseMuLatticeExhaustion {
    let census = base_mu_phase_stabilizer_census(candidate_id, b3, grid);
    let xq0 = product_x2_qa_columns(0);
    let mut t0_rediscovery_phases = Vec::new();
    let mut genuine_new_phases = Vec::new();
    for &(dx, dy) in &census.full_mu_phases {
        let f6 = f6_family_columns(dx, dy);
        if bases_are_ray_equivalent(&f6, &xq0) {
            t0_rediscovery_phases.push((dx, dy));
        } else {
            genuine_new_phases.push((dx, dy));
        }
    }
    genuine_new_phases.sort_unstable();
    let mut locked: Vec<_> = locked_genuine_seeds.to_vec();
    locked.sort_unstable();
    let genuine_new_equals_locked_seeds = genuine_new_phases == locked;
    let no_genuine_new = genuine_new_phases.is_empty();
    DiscreteF6BaseMuLatticeExhaustion {
        candidate_id: candidate_id.to_string(),
        grid_size: census.grid_size,
        full_mu_phases: census.full_mu_phases,
        t0_rediscovery_phases,
        genuine_new_phases,
        locked_genuine_seeds: locked,
        genuine_new_equals_locked_seeds,
        no_genuine_new,
        firewall:
            "exact ζ24 lattice census only; continuous (x,y) residual open; stated region only; mints no authority",
    }
}

/// Full 24×24 ζ₂₄ lattice exhaustion for the product base-MU class `{Y2⊗Q1, Y2⊗Q2}`.
pub fn exhaust_base_mu_class_full_root_of_unity_lattice() -> Vec<DiscreteF6BaseMuLatticeExhaustion>
{
    let grid = full_root_of_unity_f6_grid();
    vec![
        exhaust_base_mu_f6_lattice(
            "Y2_tensor_Q1",
            &product_y2_qa_columns(1),
            &grid,
            &genuine_dita_y2q1_triple_seeds(),
        ),
        exhaust_base_mu_f6_lattice(
            "Y2_tensor_Q2",
            &product_y2_qa_columns(2),
            &grid,
            &genuine_dita_y2q2_triple_seeds(),
        ),
    ]
}

/// Write lattice exhaustion JSON under `artifacts/`.
pub fn write_base_mu_lattice_exhaustion_artifact() -> Result<std::path::PathBuf, String> {
    let reports = exhaust_base_mu_class_full_root_of_unity_lattice();
    let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/omega_mub/artifacts");
    std::fs::create_dir_all(&dir).map_err(|e| format!("mkdir: {e}"))?;
    let path = dir.join("f6_y2q_base_mu_lattice_exhaustion_24x24_20260724.json");
    let json = serde_json::to_string_pretty(&reports).map_err(|e| format!("ser: {e}"))?;
    std::fs::write(&path, json).map_err(|e| format!("write: {e}"))?;
    Ok(path)
}

/// Run the stabilizer census for both base-MU class members on a declared grid.
pub fn base_mu_class_phase_stabilizer_report(
    grid: &[(i64, i64)],
) -> Vec<BaseMuPhaseStabilizerCensus> {
    let mut out = Vec::new();
    for a in 1..=2 {
        let id = if a == 1 {
            "Y2_tensor_Q1"
        } else {
            "Y2_tensor_Q2"
        };
        out.push(base_mu_phase_stabilizer_census(
            id,
            &product_y2_qa_columns(a),
            grid,
        ));
    }
    out
}

/// F6 probe points that are **not** ray-equivalent to product `X2⊗Q0` (the deformed chart locus).
pub fn deformed_f6_probe_grid() -> Vec<(i64, i64)> {
    let xq0 = product_x2_qa_columns(0);
    default_f6_probe_grid()
        .into_iter()
        .filter(|&(dx, dy)| {
            let f6 = f6_family_columns(dx, dy);
            !bases_are_ray_equivalent(&f6, &xq0)
        })
        .collect()
}

/// Extended corpus on the **deformed** F6 locus only (excludes T0-ray base points).
///
/// This is the load-bearing PIECE-1 residual probe: can any exact finite candidate supply an
/// external B3 for a projectively deformed F6 point?
pub fn run_extended_deformed_external_b3_gate() -> ExternalB3GateReport {
    let corpus = external_b3_extended_corpus();
    run_external_b3_gate(&deformed_f6_probe_grid(), &corpus)
}

/// Dense 24×24 root-of-unity grid (every exact `zeta_24` phase pair). Compute-heavy; keep out of
/// default unit tests unless explicitly requested.
pub fn full_root_of_unity_f6_grid() -> Vec<(i64, i64)> {
    let mut g = Vec::with_capacity(24 * 24);
    for dx in 0..24 {
        for dy in 0..24 {
            g.push((dx, dy));
        }
    }
    g
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::omega_native::exact::d6_exact_curvature_cochain::canonical_triple_exact;

    #[test]
    fn product_corpus_members_are_exact_chms() {
        for cand in external_b3_product_corpus() {
            assert!(
                basis_is_exact_chm(&cand.columns),
                "{} must be an exact CHM",
                cand.id
            );
        }
    }

    #[test]
    fn product_corpus_reproduces_canonical_t0_mu_pair() {
        // T0 = {I, X2⊗Q0, Y2⊗Q1}: the two product bases are mutually unbiased.
        let xq0 = product_x2_qa_columns(0);
        let yq1 = product_y2_qa_columns(1);
        assert!(bases_are_mutually_unbiased(&xq0, &yq1));
        // Sanity: columns match the middle/last six of the rebuilt canonical triple.
        let t0 = canonical_triple_exact();
        for i in 0..D {
            assert_eq!(t0[D + i], xq0[i]);
            assert_eq!(t0[2 * D + i], yq1[i]);
        }
    }

    #[test]
    fn f6_member_is_not_mu_to_distinct_f6_member() {
        // Regression: internal family non-MU is the reason the B3 gate is external.
        // Note: (0,0) and (8,16) are both ray-equivalent to X2⊗Q0, so they are the *same*
        // projective basis; cross-overlaps of matching rays are 1, not 1/6.
        let a = f6_family_columns(0, 0);
        let b = f6_family_columns(8, 16);
        assert!(!bases_are_mutually_unbiased(&a, &b));
    }

    #[test]
    fn f6_base_points_are_ray_equivalent_to_product_x2q0() {
        let xq0 = product_x2_qa_columns(0);
        assert!(bases_are_ray_equivalent(&f6_family_columns(0, 0), &xq0));
        assert!(bases_are_ray_equivalent(&f6_family_columns(8, 16), &xq0));
        // A deformed sample is *not* the product B2 (only the D-independent left block can match).
        assert_eq!(column_ray_match_count(&f6_family_columns(3, 7), &xq0), 3);
        assert!(!bases_are_ray_equivalent(&f6_family_columns(3, 7), &xq0));
    }

    #[test]
    fn default_external_b3_gate_finds_genuine_dita_seeds() {
        let report = run_default_external_b3_gate();
        assert_eq!(report.corpus_size, 6);
        assert_eq!(report.f6_grid_size, default_f6_probe_grid().len());
        assert_eq!(report.evaluations, report.corpus_size * report.f6_grid_size);
        assert!(report.firewall.contains("mints no authority"));
        // Locked: genuine-new seeds at F6(0,8)/(8,0)/(16,16) with Y2⊗Q1, plus T0 rediscovery.
        assert_eq!(report.terminal, ExternalB3GateTerminal::GenuineNewSeedFound);
        assert!(report.genuine_new_seed_count >= 3);
        assert!(report.t0_rediscovery_count >= 2);
        let genuine: Vec<_> = report
            .hits
            .iter()
            .filter(|h| h.class == ExternalB3HitClass::GenuineNewF6Seed)
            .collect();
        assert!(genuine.iter().all(|h| h.candidate_id == "Y2_tensor_Q1"));
        for &(dx, dy) in &genuine_dita_y2q1_triple_seeds() {
            assert!(
                genuine.iter().any(|h| h.f6_dx == dx && h.f6_dy == dy),
                "missing genuine seed F6({dx},{dy})"
            );
        }
        // Generic deformed probes remain non-MU.
        let yq1 = product_y2_qa_columns(1);
        for &(dx, dy) in &[(3_i64, 7), (5, 13), (1, 1)] {
            assert!(!bases_are_mutually_unbiased(
                &f6_family_columns(dx, dy),
                &yq1
            ));
        }
    }

    #[test]
    fn genuine_dita_seeds_are_exact_mu_triples_not_t0_ray() {
        let xq0 = product_x2_qa_columns(0);
        let yq1 = product_y2_qa_columns(1);
        for &(dx, dy) in &genuine_dita_y2q1_triple_seeds() {
            let f6 = f6_family_columns(dx, dy);
            assert!(f6_point_is_exact_chm(dx, dy));
            assert!(basis_is_exact_chm(&yq1));
            assert!(bases_are_mutually_unbiased(&f6, &yq1));
            assert_eq!(column_ray_match_count(&f6, &xq0), 3);
            assert!(!bases_are_ray_equivalent(&f6, &xq0));
        }
    }

    #[test]
    fn swapped_and_butson_corpus_members_are_exact_chms() {
        for cand in external_b3_swapped_product_corpus() {
            assert!(
                basis_is_exact_chm(&cand.columns),
                "{} must be an exact CHM",
                cand.id
            );
        }
        let butson = external_b3_butson_corpus();
        assert!(
            !butson.is_empty(),
            "butson corpus must retain at least one exact CHM"
        );
        for cand in &butson {
            assert!(
                basis_is_exact_chm(&cand.columns),
                "{} must be an exact CHM",
                cand.id
            );
        }
    }

    #[test]
    fn swapped_product_is_ray_distinct_from_qubit_qutrit_product() {
        // Swapped identification is a different block layout; not ray-equivalent to X2⊗Q0.
        let xq0 = product_x2_qa_columns(0);
        let qx = product_qa_x2_columns(0);
        assert!(!bases_are_ray_equivalent(&xq0, &qx));
        assert!(column_ray_match_count(&xq0, &qx) < D);
    }

    #[test]
    fn f6_left_block_is_phase_independent_on_probe_grid() {
        for &(dx, dy) in &default_f6_probe_grid() {
            assert!(
                f6_left_block_independent_of_phases(dx, dy),
                "left block of F6({dx},{dy}) must match F6(0,0) rays"
            );
        }
    }

    #[test]
    fn extended_deformed_gate_finds_genuine_dita_seeds() {
        let report = run_extended_deformed_external_b3_gate();
        assert!(
            report.corpus_size > 6,
            "extended corpus larger than product-only"
        );
        assert!(!deformed_f6_probe_grid().is_empty());
        assert_eq!(report.f6_grid_size, deformed_f6_probe_grid().len());
        // Deformed grid excludes T0-ray points, so rediscovery count must be zero.
        assert_eq!(report.t0_rediscovery_count, 0);
        // Locked: genuine Dita seeds appear on the deformed grid (Y2⊗Q1 @ (0,8),(8,0),(16,16)).
        assert_eq!(report.terminal, ExternalB3GateTerminal::GenuineNewSeedFound);
        assert!(report.genuine_new_seed_count >= 3);
        assert!(report.firewall.contains("mints no authority"));
    }

    #[test]
    fn mu_to_f6_implies_base_left_triad_holds_for_extended_corpus() {
        let corpus = external_b3_extended_corpus();
        for &(dx, dy) in &default_f6_probe_grid() {
            for cand in &corpus {
                assert!(
                    mu_to_f6_implies_mu_to_base_left_triad(dx, dy, &cand.columns),
                    "necessity lemma failed for {} at F6({},{})",
                    cand.id,
                    dx,
                    dy
                );
            }
        }
    }

    #[test]
    fn product_y2_hits_right_block_only_obstruction_on_nonseed_deformed_f6() {
        let report = product_y2_deformed_right_block_obstruction_report();
        assert!(!report.is_empty());
        let seeds = genuine_dita_y2q1_triple_seeds();
        for cert in &report {
            assert!(
                cert.left_triad_mu,
                "{} at F6({},{}) should pass left triad",
                cert.candidate_id, cert.f6_dx, cert.f6_dy
            );
            let is_y2q1_seed = cert.candidate_id == "Y2_tensor_Q1"
                && seeds
                    .iter()
                    .any(|&(dx, dy)| dx == cert.f6_dx && dy == cert.f6_dy);
            if is_y2q1_seed {
                assert!(cert.full_mu);
                continue;
            }
            assert!(!cert.full_mu);
            assert!(!cert.right_triad_mu);
            assert!(
                cert.right_block_only_obstruction,
                "{} at F6({},{}) should be right-block-only obstruction; first={:?}",
                cert.candidate_id, cert.f6_dx, cert.f6_dy, cert.first_failure
            );
            let (i, _) = cert.first_failure.expect("failure witness");
            assert!(i >= 3, "first failure must be a right-block F6 column");
        }
    }

    #[test]
    fn full_mu_iff_left_and_right_triad_mu() {
        let f6 = f6_family_columns(3, 7);
        let yq1 = product_y2_qa_columns(1);
        let xq0 = product_x2_qa_columns(0);
        // Non-MU pair: left may hold without full MU.
        assert_eq!(
            bases_are_mutually_unbiased(&f6, &yq1),
            is_mu_to_f6_left_triad(&f6, &yq1) && is_mu_to_f6_right_triad(&f6, &yq1)
        );
        // Self MU (same basis) is not MU-to-distinct; xq0 vs f6 at deformed is not full MU.
        assert_eq!(
            bases_are_mutually_unbiased(&f6, &xq0),
            is_mu_to_f6_left_triad(&f6, &xq0) && is_mu_to_f6_right_triad(&f6, &xq0)
        );
        // At the base point, Y2⊗Q1 is fully MU to F6(0,0) ~ X2⊗Q0.
        let f00 = f6_family_columns(0, 0);
        assert!(bases_are_mutually_unbiased(&f00, &yq1));
        assert!(is_mu_to_f6_left_triad(&f00, &yq1) && is_mu_to_f6_right_triad(&f00, &yq1));
    }

    #[test]
    fn base_mu_class_is_exactly_product_y2_q1_q2() {
        // Locked classification of the extended finite corpus at F6(0,0):
        // only Y2⊗Q1 and Y2⊗Q2 complete an MU triple with the base chart point.
        let class = extended_corpus_mu_to_base_f6();
        let mut ids: Vec<&str> = class.iter().map(|c| c.id).collect();
        ids.sort();
        assert_eq!(ids, vec!["Y2_tensor_Q1", "Y2_tensor_Q2"]);
    }

    #[test]
    fn base_mu_class_split_on_deformed_grid_separates_seeds_from_obstructions() {
        let report = base_mu_class_deformed_obstruction_report();
        assert_eq!(report.base_mu_class_size, 2);
        assert_eq!(report.deformed_grid_size, deformed_f6_probe_grid().len());
        assert!(!report.certificates.is_empty());
        // Genuine Dita seeds for Y2⊗Q1 appear as full_mu on the deformed grid.
        assert!(report.any_full_mu_on_deformed);
        assert!(!report.all_right_block_only);
        assert!(report.firewall.contains("mints no authority"));
        let seeds = genuine_dita_y2q1_triple_seeds();
        for cert in &report.certificates {
            assert!(
                cert.left_triad_mu,
                "left triad always holds for base-MU class"
            );
            let b3 = if cert.candidate_id == "Y2_tensor_Q1" {
                product_y2_qa_columns(1)
            } else {
                product_y2_qa_columns(2)
            };
            let is_y2q1_seed = cert.candidate_id == "Y2_tensor_Q1"
                && seeds
                    .iter()
                    .any(|&(dx, dy)| dx == cert.f6_dx && dy == cert.f6_dy);
            if is_y2q1_seed {
                assert!(cert.full_mu);
                assert!(cert.right_triad_mu);
                assert!(right_triad_residual_is_zero(cert.f6_dx, cert.f6_dy, &b3));
            } else if cert.candidate_id == "Y2_tensor_Q2"
                || !seeds
                    .iter()
                    .any(|&(dx, dy)| dx == cert.f6_dx && dy == cert.f6_dy)
            {
                // Non-seed deformed points: right-block obstruction for both class members.
                if cert.candidate_id == "Y2_tensor_Q2" || !is_y2q1_seed {
                    // For Y2Q1 at non-seed deformed points, or any Y2Q2 deformed point:
                    if !(cert.candidate_id == "Y2_tensor_Q1" && is_y2q1_seed) {
                        assert!(
                            !cert.full_mu,
                            "unexpected full MU for {} at F6({},{})",
                            cert.candidate_id, cert.f6_dx, cert.f6_dy
                        );
                    }
                }
            }
            assert!(right_triad_residual_is_zero(0, 0, &b3));
        }
        // Explicit: every genuine seed cert is present and fully MU.
        for &(dx, dy) in &seeds {
            let hit = report
                .certificates
                .iter()
                .find(|c| c.candidate_id == "Y2_tensor_Q1" && c.f6_dx == dx && c.f6_dy == dy);
            assert!(hit.unwrap().full_mu);
        }
    }

    #[test]
    fn right_dephasing_formula_matches_f6_assembly() {
        let yq1 = product_y2_qa_columns(1);
        for &(dx, dy) in &[(0_i64, 0), (8, 16), (3, 7), (5, 13), (1, 1)] {
            assert!(
                right_dephasing_formula_matches_assembly(dx, dy, &yq1),
                "dephasing formula must match assembly at F6({dx},{dy})"
            );
        }
        // Also against a non-base-MU candidate (formula is structural, not class-specific).
        let qx = product_qa_x2_columns(0);
        assert!(right_dephasing_formula_matches_assembly(3, 7, &qx));
    }

    #[test]
    fn base_mu_phase_stabilizer_y2q1_has_genuine_orbit_on_default_grid() {
        let reports = base_mu_class_phase_stabilizer_report(&default_f6_probe_grid());
        assert_eq!(reports.len(), 2);
        let q1 = reports
            .iter()
            .find(|c| c.candidate_id == "Y2_tensor_Q1")
            .unwrap();
        let q2 = reports
            .iter()
            .find(|c| c.candidate_id == "Y2_tensor_Q2")
            .unwrap();
        // Y2⊗Q1: base-ray phases plus genuine seeds (0,8)/(8,0)/(16,16).
        assert!(q1.base_ray_class_subseteq_full_mu);
        assert!(!q1.full_mu_subseteq_base_ray_class);
        assert!(q1.full_mu_count > q1.ray_equivalent_to_base_count);
        for &(dx, dy) in &genuine_dita_y2q1_triple_seeds() {
            assert!(q1.full_mu_phases.contains(&(dx, dy)));
        }
        // Y2⊗Q2: default probe grid does not include the dual genuine orbit
        // {(0,16),(8,8),(16,0)}; on that limited grid it may look base-ray-only.
        assert!(q2.base_ray_class_subseteq_full_mu);
    }

    /// Dense 12×12 census (step=2): both Y2⊗Q{1,2} genuine-new orbits match locked seeds.
    #[test]
    fn base_mu_phase_stabilizer_on_step2_root_of_unity_grid() {
        let grid = root_of_unity_f6_grid_step(2);
        assert_eq!(grid.len(), 12 * 12);
        let q1 = exhaust_base_mu_f6_lattice(
            "Y2_tensor_Q1",
            &product_y2_qa_columns(1),
            &grid,
            &genuine_dita_y2q1_triple_seeds(),
        );
        let q2 = exhaust_base_mu_f6_lattice(
            "Y2_tensor_Q2",
            &product_y2_qa_columns(2),
            &grid,
            &genuine_dita_y2q2_triple_seeds(),
        );
        assert!(
            q1.genuine_new_equals_locked_seeds,
            "q1 genuine={:?}",
            q1.genuine_new_phases
        );
        assert!(
            q2.genuine_new_equals_locked_seeds,
            "q2 genuine={:?}",
            q2.genuine_new_phases
        );
        assert_eq!(q1.genuine_new_phases, genuine_dita_y2q1_triple_seeds());
        assert_eq!(q2.genuine_new_phases, genuine_dita_y2q2_triple_seeds());
        assert!(!q1.t0_rediscovery_phases.is_empty());
        assert!(!q2.t0_rediscovery_phases.is_empty());
    }

    /// Full 24×24 ζ₂₄ lattice exhaustion (~40s release). Run: `--ignored --nocapture`.
    #[test]
    #[ignore = "heavy: exact 24×24 F6 lattice census for Y2⊗Q{1,2}"]
    fn base_mu_full_root_of_unity_lattice_exhaustion() {
        let reports = exhaust_base_mu_class_full_root_of_unity_lattice();
        assert_eq!(reports.len(), 2);
        let q1 = reports
            .iter()
            .find(|c| c.candidate_id == "Y2_tensor_Q1")
            .unwrap();
        let q2 = reports
            .iter()
            .find(|c| c.candidate_id == "Y2_tensor_Q2")
            .unwrap();
        assert_eq!(q1.grid_size, 24 * 24);
        // Discrete lattice theorem: genuine-new orbits are exactly the locked seed sets.
        assert!(
            q1.genuine_new_equals_locked_seeds,
            "Y2Q1 unexpected genuine-new: {:?}",
            q1.genuine_new_phases
        );
        assert!(
            q2.genuine_new_equals_locked_seeds,
            "Y2Q2 unexpected genuine-new: {:?}",
            q2.genuine_new_phases
        );
        assert_eq!(q1.genuine_new_phases, genuine_dita_y2q1_triple_seeds());
        assert_eq!(q2.genuine_new_phases, genuine_dita_y2q2_triple_seeds());
        assert!(!q1.t0_rediscovery_phases.is_empty());
        assert!(!q2.t0_rediscovery_phases.is_empty());
        let path = write_base_mu_lattice_exhaustion_artifact().expect("write artifact");
        assert!(path.exists());
        eprintln!(
            "Y2Q1 genuine={:?} t0_redisc={}; Y2Q2 genuine={:?}; artifact={}",
            q1.genuine_new_phases,
            q1.t0_rediscovery_phases.len(),
            q2.genuine_new_phases,
            path.display()
        );
    }
}
