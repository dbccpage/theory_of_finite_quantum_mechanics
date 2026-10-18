//! Phase-0b exact **deformation-invariance probe** for the MUB(6) fourth-vector problem,
//! over the native field `Q(zeta_24)`.
//!
//! Phase 0 (`d6_exact_deformation_invariance_probe`) showed that the two ω-BLIND
//! cohomological invariants `rank(J)` and `dim H^1` FAIL the bypass: they are rigid-but-blind
//! (a would-be near-MU flat sample and a far control can carry the SAME exact curvature mass
//! `1/2` yet DIFFERENT pairs `(11, 5)` vs `(10, 6)`, and `H^1 >= 5` never vanishes, so the
//! invariant cannot certify emptiness by degenerating). Those invariants only see the tangent
//! Jacobian `J`, never the actual curvature `omega(v)`.
//!
//! Phase-0b probes invariants that DO see the actual curvature `omega(v)` — invariants that
//! therefore have a real shot at property (a) (no-go-certifying):
//!
//!   1. **`first_order_repairable(v)` [EXACT, gate-deciding]:** is `omega(v) in im(J)`? i.e.
//!      does `solve_exact(J, -omega)` return `Some(x)`? If so the curvature residual can be
//!      cancelled to first order; if `None` the curvature is first-order OBSTRUCTED. This is
//!      the vanishing of the `H^1`-class OF THE ACTUAL CURVATURE, not the dimension of `H^1`.
//!   2. **`kuranishi_extends(v)` [EXACT, gate-deciding; N/A if not repairable]:** convert the
//!      first-order repair `x` (real coords) to a complex deformation
//!      `dv_repair[k] = x[2k] + i x[2k+1]`; does that repair extend past second order
//!      (`Q(dv_repair) in im(J)`, the Maurer-Cartan/Kuranishi obstruction)?
//!   3. **`degree_winding(v)` [NUMERIC DIAGNOSTIC ONLY — decides NO gate]:** the integer
//!      winding number of `t -> (Re a, Im a)`, `a = <e_6, v(t)>`, as `v(t)` sweeps one phase
//!      circle. Illustrative only (see the principled degree note below).
//!
//! Same disciplined loop as Phase 0: **exact arithmetic decides every gate; `f64` is used
//! ONLY for the human-readable columns** (a numeric evaluation of a cyclotomic number) and the
//! purely-illustrative winding, never to decide a gate. We reuse Phase 0's EXACT 14-candidate
//! set verbatim (2 far controls + 12 flat 5-torus samples) so the two probes are comparable.
//!
//! Two gates, evaluated for BOTH exact invariants:
//!
//!   * **Gate A (no-go link):** does the invariant TRACK the scalar no-go? (A1) do two
//!     candidates with EQUAL exact curvature mass ever carry DIFFERENT invariant values? (if
//!     so the invariant is not even a function of the scalar and cannot track it). (A2) do the
//!     most-MU-like flat samples' invariants DIFFER from the far controls'? Gate A passes only
//!     if no exact mass-collision decouples the invariant AND near-MU samples move it.
//!   * **Gate B (rigidity):** is the invariant CONSTANT across the flat 5-torus samples, or
//!     does it jump? The flat samples off the modal value are the vector-level wall locus `W`.
//!
//! Terminal: `OpenResidual`. Phase-0b mints NO authority; it only decides which candidate
//! invariant survives.
//!
//! # Firewall
//!
//! module can issue is `OpenResidual`. As in Phase 0, this is the vector-level probe for the
//! FIXED canonical triple `T0` (sweeping the candidate fourth-vector over the gauge-fixed
//! 5-torus); a triple-level deformation path across the moduli needs a second inequivalent
//! exact MU triple we do not yet have.
//!
//! # Principled degree note (verbatim)
//!
//! Degree / topological-forcing invariants certify EXISTENCE of a zero (nonzero degree ==> a
//! fourth MU vector exists), not EMPTINESS (no MU vector). The no-go is emptiness =
//! non-existence, so no nonzero value of a standard degree can certify it (emptiness ==>
//! degree 0, but degree 0 is consistent with both). Additionally, an EXACT degree needs
//! certified real-sign determination, which the equality-based Cyc24 toolkit does not provide
//! (it decides is_zero, not sign). The winding computed here is therefore a NUMERIC diagnostic
//! only; it decides no gate. The emptiness question is quantitative/algebraic (the scalar wall
//! Phi > 0, or an exact SOS/Positivstellensatz certificate), not topological.

use std::fmt::Debug;

use num_rational::BigRational;
use num_traits::ToPrimitive;

use crate::omega_native::exact::d6_exact_curvature_cochain::{
    abs_sq, as_rational, canonical_triple_exact, cmp_exact_real, curvature_c2, norm_sq, ExactVec, D,
};
use crate::omega_native::exact::d6_exact_deformation_invariance_probe::{
    candidate_set, inv_sqrt6, SampleCategory,
};
use crate::omega_native::exact::d6_exact_lift_repair::solve_exact;
use crate::omega_native::exact::d6_exact_maurer_cartan::second_order_obstruction;
use crate::omega_native::exact::d6_exact_tangent_obstruction::{curvature_jacobian, mat_vec};
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::ri;

/// **Reporting-only** numeric complex embedding of a cyclotomic number: evaluate
/// `sum_k a_k zeta^k` at `zeta = e^{2 pi i / 24}` and return `(Re, Im)`. Used ONLY for the
/// human-readable table columns and the illustrative winding; never to decide a gate.
fn numeric_complex(z: &Cyc24) -> (f64, f64) {
    let mut re = 0.0f64;
    let mut im = 0.0f64;
    for (k, a) in z.a.iter().enumerate() {
        let ak = a.to_f64().unwrap_or(f64::NAN);
        let ang = std::f64::consts::PI * (k as f64) / 12.0; // 2 pi k / 24
        re += ak * ang.cos();
        im += ak * ang.sin();
    }
    (re, im)
}

/// Reporting-only numeric real part.
fn numeric_re(z: &Cyc24) -> f64 {
    numeric_complex(z).0
}

/// **NUMERIC DIAGNOSTIC ONLY (decides no gate).** The integer winding number of
/// `t -> (Re a(t), Im a(t))`, `a(t) = <e_6, v(t)>` (the first B2 overlap), as `v(t)` sweeps a
/// torus loop that continuously varies ONE phase: coordinate 1 becomes
/// `v_1(t) = inv_sqrt6 * e^{2 pi i t / 24}`, all other coordinates held at `v`'s numeric
/// values, `t: 0 -> 24` (one full circle). Counted numerically in the float embedding. See the
/// principled degree note in the module doc: this is illustrative only.
///
/// Returns `None` (undefined) if the circle passes through the origin (|centre|^2 == |amplitude|^2, R10).
fn degree_winding(columns: &[ExactVec], v: &ExactVec) -> Option<i64> {
    // Exact check for circle passing through origin (R10):
    // a(theta) = centre + amp * exp(i theta)
    // where centre = sum_{k != 1} conj(columns[6][k]) * v[k]
    // amp = conj(columns[6][1]) * inv_sqrt6()
    let mut centre = Cyc24::zero();
    for k in 0..D {
        if k != 1 {
            centre = centre.add(&columns[6][k].conj().mul(&v[k]));
        }
    }
    let amp = columns[6][1].conj().mul(&inv_sqrt6());
    if abs_sq(&centre) == abs_sq(&amp) {
        return None; // Loop passes through origin: winding is undefined
    }

    // e_6 = column index 6 = first B2 vector.
    let e6: Vec<(f64, f64)> = columns[6].iter().map(numeric_complex).collect();
    let vc: Vec<(f64, f64)> = v.iter().map(numeric_complex).collect();
    let r = numeric_re(&inv_sqrt6()); // magnitude of the swept coordinate, |v_1(t)| = 1/sqrt6
    let steps = 8192usize;
    let two_pi = 2.0 * std::f64::consts::PI;
    let mut prev_ang: Option<f64> = None;
    let mut total = 0.0f64;
    for s in 0..=steps {
        let t = 24.0 * (s as f64) / (steps as f64);
        let phase = std::f64::consts::PI * t / 12.0; // 2 pi t / 24
        let (mut are, mut aim) = (0.0f64, 0.0f64);
        for k in 0..D {
            let (vre, vim) = if k == 1 {
                (r * phase.cos(), r * phase.sin())
            } else {
                vc[k]
            };
            // a += conj(e6[k]) * v_k = (ere, -eim) * (vre, vim)
            let (ere, eim) = e6[k];
            are += ere * vre + eim * vim;
            aim += ere * vim - eim * vre;
        }
        let ang = aim.atan2(are);
        if let Some(p) = prev_ang {
            let mut d = ang - p;
            while d > std::f64::consts::PI {
                d -= two_pi;
            }
            while d < -std::f64::consts::PI {
                d += two_pi;
            }
            total += d;
        }
        prev_ang = Some(ang);
    }
    Some((total / two_pi).round() as i64)
}

/// One computed row of the Phase-0b probe table.
#[derive(Clone, Debug)]
pub struct SampleRowB {
    pub label: String,
    pub category: SampleCategory,
    /// `norm_sq(v) == 1` exactly (construction invariant; asserted in the harness).
    pub is_unit: bool,
    /// Curvature mass `sum_i |omega_i|^2`, exact rational when rational.
    pub omega_mass_rational: Option<BigRational>,
    /// Reporting-only numeric curvature mass.
    pub omega_mass_float: f64,
    /// Gate-internal EXACT curvature mass (for the exact mass-collision falsification).
    pub omega_mass_exact: Cyc24,
    /// **EXACT, gate-deciding.** `omega(v) in im(J)` — the curvature can be cancelled to first
    /// order (its `H^1`-class vanishes).
    pub first_order_repairable: bool,
    /// Structural: when repairable, `J . x == -omega(v)` re-verified exactly.
    pub repair_verified: Option<bool>,
    /// **EXACT, gate-deciding; `None` iff not first-order-repairable.** Does the first-order
    /// repair extend past second order (`Q(dv_repair) in im(J)`, Kuranishi obstruction)?
    pub kuranishi_extends: Option<bool>,
    /// Sanity: the MC quadratic bracket is Bianchi-closed (must be true when computed).
    pub bianchi_closed: Option<bool>,
    /// **NUMERIC diagnostic only (decides no gate).** Winding number of the first-B2 overlap (`None` if loop crosses zero).
    pub degree_winding: Option<i64>,
}

impl SampleRowB {
    /// Invariant 1 value: `first_order_repairable` (bool).
    fn inv_repairable(&self) -> bool {
        self.first_order_repairable
    }
    /// Invariant 2 value: `kuranishi_extends` (Option<bool>; `None` = N/A).
    fn inv_kuranishi(&self) -> Option<bool> {
        self.kuranishi_extends
    }
}

/// Tri-state gate status separating evaluated pass/fail from inapplicable outcomes (R09).
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
pub enum GateStatus {
    Pass,
    Fail,
    NotApplicable,
}

pub trait InvariantValue {
    fn is_applicable(&self) -> bool {
        true
    }
}

impl InvariantValue for bool {
    fn is_applicable(&self) -> bool {
        true
    }
}

impl<U> InvariantValue for Option<U> {
    fn is_applicable(&self) -> bool {
        self.is_some()
    }
}

impl InvariantValue for usize {
    fn is_applicable(&self) -> bool {
        true
    }
}

impl InvariantValue for String {
    fn is_applicable(&self) -> bool {
        true
    }
}

/// A gate verdict for one invariant.
#[derive(Clone, Debug)]
pub struct GateVerdict {
    pub pass: bool,
    pub status: GateStatus,
    pub reason: String,
    /// Flat samples off the modal value (Gate B wall locus); empty for Gate A.
    pub wall_samples: Vec<String>,
    pub applicable_count: usize,
    pub total_count: usize,
}

/// The full Phase-0b probe report: per-candidate rows and Gate A/B for BOTH exact invariants.
#[derive(Clone, Debug)]
pub struct ProbeReportB {
    pub rows: Vec<SampleRowB>,
    pub repairable_gate_a: GateVerdict,
    pub repairable_gate_b: GateVerdict,
    pub kuranishi_gate_a: GateVerdict,
    pub kuranishi_gate_b: GateVerdict,
    /// Phase-0b's only terminal.
    pub terminal: &'static str,
}

/// Compute one exact row for a candidate vector.
fn compute_row_b(
    columns: &[ExactVec],
    label: &str,
    category: SampleCategory,
    v: &ExactVec,
) -> SampleRowB {
    let is_unit = norm_sq(v) == Cyc24::rat(ri(1));

    let omega = curvature_c2(columns, v);
    let mut mass = Cyc24::zero();
    for w in &omega {
        mass = mass.add(&abs_sq(w));
    }

    // Invariant 1 (EXACT): is omega(v) in im(J)? Solve J . x = -omega exactly.
    let j = curvature_jacobian(columns, v);
    let neg_omega: Vec<Cyc24> = omega.iter().map(|w| w.neg()).collect();
    let repair = solve_exact(&j, &neg_omega).ok().flatten();
    let first_order_repairable = repair.is_some();

    // Invariant 2 (EXACT; N/A if not repairable): does the first-order repair extend to
    // second order? Convert the real repair x (length 12) to a complex deformation dv (length
    // 6) and test the Kuranishi obstruction.
    let mut repair_verified = None;
    let mut kuranishi_extends = None;
    let mut bianchi_closed = None;
    if let Some(x) = &repair {
        // Re-verify the first-order repair cancels the residual exactly.
        repair_verified = Some(mat_vec(&j, x).expect("jacobian shape") == neg_omega);
        // dv_repair[k] = x[2k] + i x[2k+1], with i = zeta_24^6.
        let i = Cyc24::zeta24(6);
        let dv: ExactVec = std::array::from_fn(|k| x[2 * k].add(&i.mul(&x[2 * k + 1])));
        let so = second_order_obstruction(columns, v, &dv);
        bianchi_closed = Some(so.bianchi_closed);
        kuranishi_extends = Some(so.second_order_absorbable);
    }

    // Invariant 3 (NUMERIC diagnostic only).
    let degree_winding = degree_winding(columns, v);

    SampleRowB {
        label: label.to_string(),
        category,
        is_unit,
        omega_mass_rational: as_rational(&mass),
        omega_mass_float: numeric_re(&mass),
        omega_mass_exact: mass,
        first_order_repairable,
        repair_verified,
        kuranishi_extends,
        bianchi_closed,
        degree_winding,
    }
}

/// The most-frequent value (mode) of a slice; `None` if empty.
fn mode<T: PartialEq + Clone>(vals: &[T]) -> Option<T> {
    let mut best: Option<(T, usize)> = None;
    for v in vals {
        let count = vals.iter().filter(|&x| x == v).count();
        match &best {
            Some((_, bc)) if *bc >= count => {}
            _ => best = Some((v.clone(), count)),
        }
    }
    best.map(|(v, _)| v)
}

/// **Gate A (sampled link)** for a generic invariant `inv`.
///
/// Passes only if (A1) NO two candidates with equal EXACT curvature mass carry different
/// invariant values (else the invariant is not a function of the scalar curvature mass) AND (A2) the
/// most-MU-like third of the flat samples (ordered by exact mass) carry an
/// invariant value the far controls do not (flatness/MU-proximity must MOVE the invariant).
fn eval_gate_a<T, F>(rows: &[SampleRowB], name: &str, inv: F) -> GateVerdict
where
    T: InvariantValue + PartialEq + Clone + Debug,
    F: Fn(&SampleRowB) -> T,
{
    let total_count = rows.len();
    let applicable_count = rows.iter().filter(|r| inv(r).is_applicable()).count();
    if applicable_count == 0 {
        return GateVerdict {
            pass: false,
            status: GateStatus::NotApplicable,
            reason: format!(
                "{name} has 0 applicable observations out of {total_count} samples => Gate A FAIL (NotApplicable)"
            ),
            wall_samples: Vec::new(),
            applicable_count: 0,
            total_count,
        };
    }

    // (A1) exact mass-collision that decouples the invariant.
    let mut collision: Option<(String, String, T, T)> = None;
    'scan: for i in 0..rows.len() {
        for j in (i + 1)..rows.len() {
            let vi = inv(&rows[i]);
            let vj = inv(&rows[j]);
            if vi.is_applicable()
                && vj.is_applicable()
                && rows[i].omega_mass_exact == rows[j].omega_mass_exact
                && vi != vj
            {
                collision = Some((rows[i].label.clone(), rows[j].label.clone(), vi, vj));
                break 'scan;
            }
        }
    }

    let far_vals: Vec<T> = rows
        .iter()
        .filter(|r| r.category == SampleCategory::FarControl)
        .map(&inv)
        .filter(|v| v.is_applicable())
        .collect();
    let mut flat: Vec<&SampleRowB> = rows
        .iter()
        .filter(|r| r.category == SampleCategory::FlatTorus)
        .collect();
    flat.sort_by(|a, b| cmp_exact_real(&a.omega_mass_exact, &b.omega_mass_exact));
    let near_count = (flat.len() / 3).max(1);
    let near: Vec<&SampleRowB> = flat.iter().take(near_count).copied().collect();
    let near_vals: Vec<T> = near
        .iter()
        .map(|r| inv(r))
        .filter(|v| v.is_applicable())
        .collect();
    let near_differs = !near_vals.is_empty() && near_vals.iter().any(|v| !far_vals.contains(v));

    let pass = collision.is_none() && near_differs;
    let status = if pass {
        GateStatus::Pass
    } else {
        GateStatus::Fail
    };
    let reason = if let Some((li, lj, vi, vj)) = &collision {
        format!(
            "EXACT decoupling: '{li}' and '{lj}' have IDENTICAL exact curvature mass yet \
             {name} = {vi:?} vs {vj:?} => sampled {name} does not factor through scalar curvature mass on this population => Gate A FAIL"
        )
    } else if !near_differs {
        format!(
            "the most-MU-like flat samples {:?} carry {name} values {:?}, all already present in \
             the far controls {:?} => flatness/MU-proximity does not move {name} => Gate A FAIL",
            near.iter().map(|r| r.label.as_str()).collect::<Vec<_>>(),
            near_vals,
            far_vals,
        )
    } else {
        format!(
            "near-MU flat samples move {name} away from the far-control values and no exact \
             mass-collision decouples it => Gate A SIGNAL"
        )
    };
    GateVerdict {
        pass,
        status,
        reason,
        wall_samples: Vec::new(),
        applicable_count,
        total_count,
    }
}

/// **Gate B (rigidity)** for a generic invariant `inv`: is it CONSTANT across the flat 5-torus
/// samples? The flat samples off the modal value are the wall locus.
fn eval_gate_b<T, F>(rows: &[SampleRowB], name: &str, inv: F) -> GateVerdict
where
    T: InvariantValue + PartialEq + Clone + Debug,
    F: Fn(&SampleRowB) -> T,
{
    let flat: Vec<&SampleRowB> = rows
        .iter()
        .filter(|r| r.category == SampleCategory::FlatTorus)
        .collect();
    let total_count = flat.len();
    let applicable: Vec<(&SampleRowB, T)> = flat
        .iter()
        .map(|&r| (r, inv(r)))
        .filter(|(_, v)| v.is_applicable())
        .collect();
    let applicable_count = applicable.len();

    if applicable_count == 0 {
        return GateVerdict {
            pass: false,
            status: GateStatus::NotApplicable,
            reason: format!(
                "{name} has 0 applicable observations out of {total_count} flat 5-torus samples => \
                 NotApplicable (vacuous constancy rejected)"
            ),
            wall_samples: Vec::new(),
            applicable_count: 0,
            total_count,
        };
    }

    let vals: Vec<T> = applicable.iter().map(|(_, v)| v.clone()).collect();
    let modal = mode(&vals);
    let wall_samples: Vec<String> = applicable
        .iter()
        .filter(|(_, v)| Some(v) != modal.as_ref())
        .map(|(r, _)| r.label.clone())
        .collect();
    let pass = wall_samples.is_empty();
    let status = if pass {
        GateStatus::Pass
    } else {
        GateStatus::Fail
    };
    let reason = if pass {
        format!(
            "{name} is constant = {:?} across all {} applicable flat 5-torus samples ({}/{}) => rigid, no \
             vector-level wall-crossing observed",
            modal,
            applicable_count,
            applicable_count,
            total_count
        )
    } else {
        format!(
            "{name} jumps off the modal value {:?} at {} flat sample(s) {:?} => vector-level \
             wall locus W is non-empty",
            modal,
            wall_samples.len(),
            wall_samples
        )
    };
    GateVerdict {
        pass,
        status,
        reason,
        wall_samples,
        applicable_count,
        total_count,
    }
}

/// Run the exact Phase-0b deformation-invariance probe.
pub fn run_probe_b() -> ProbeReportB {
    let columns = canonical_triple_exact();
    let candidates = candidate_set();

    let rows: Vec<SampleRowB> = candidates
        .iter()
        .map(|(label, cat, v)| compute_row_b(&columns, label, *cat, v))
        .collect();

    let repairable_gate_a =
        eval_gate_a(&rows, "first_order_repairable", SampleRowB::inv_repairable);
    let repairable_gate_b =
        eval_gate_b(&rows, "first_order_repairable", SampleRowB::inv_repairable);
    let kuranishi_gate_a = eval_gate_a(&rows, "kuranishi_extends", SampleRowB::inv_kuranishi);
    let kuranishi_gate_b = eval_gate_b(&rows, "kuranishi_extends", SampleRowB::inv_kuranishi);

    ProbeReportB {
        rows,
        repairable_gate_a,
        repairable_gate_b,
        kuranishi_gate_a,
        kuranishi_gate_b,
        terminal: "OpenResidual",
    }
}

/// Format an optional exact rational for the table.
fn fmt_rat(r: &Option<BigRational>) -> String {
    match r {
        Some(q) => format!("{q}"),
        None => "non-rational-cyc".to_string(),
    }
}

fn fmt_opt_bool(b: &Option<bool>) -> String {
    match b {
        Some(true) => "yes".to_string(),
        Some(false) => "no".to_string(),
        None => "N/A".to_string(),
    }
}

fn fmt_opt_i64(b: &Option<i64>) -> String {
    match b {
        Some(v) => format!("{v}"),
        None => "undef".to_string(),
    }
}

/// Render the full Phase-0b probe table as a printable string (reporting only).
pub fn render_table_b(report: &ProbeReportB) -> String {
    let mut s = String::new();
    s.push_str("=== MUB(6) Phase-0b exact curvature-seeing deformation-invariance probe ===\n");
    s.push_str("(vector-level, fixed canonical triple T0; exact decides gates, f64 reports)\n\n");
    s.push_str(&format!(
        "{:<14} {:<5} {:<6} {:<18} {:<12} {:>10} {:>10} {:>8} {:>8} {:>8}\n",
        "label",
        "cat",
        "unit",
        "mass (exact)",
        "mass(~f64)",
        "repairable",
        "kuranishi",
        "winding",
        "repairOK",
        "bianchi",
    ));
    for r in &report.rows {
        let cat = match r.category {
            SampleCategory::FarControl => "far",
            SampleCategory::FlatTorus => "flat",
        };
        s.push_str(&format!(
            "{:<14} {:<5} {:<6} {:<18} {:<12.6} {:>10} {:>10} {:>8} {:>8} {:>8}\n",
            r.label,
            cat,
            r.is_unit,
            fmt_rat(&r.omega_mass_rational),
            r.omega_mass_float,
            r.first_order_repairable,
            fmt_opt_bool(&r.kuranishi_extends),
            fmt_opt_i64(&r.degree_winding),
            fmt_opt_bool(&r.repair_verified),
            fmt_opt_bool(&r.bianchi_closed),
        ));
    }

    s.push_str("\n--- Gate verdicts (EXACT invariants) ---\n");
    let g = |title: &str, a: &GateVerdict, b: &GateVerdict| -> String {
        format!(
            "[{title}]\n  Gate A (sampled link): {}\n    {}\n  Gate B (rigidity):     {}\n    {}\n",
            match a.status {
                GateStatus::Pass => "SIGNAL",
                GateStatus::Fail => "FAIL",
                GateStatus::NotApplicable => "N/A",
            },
            a.reason,
            match b.status {
                GateStatus::Pass => "RIGID",
                GateStatus::Fail => "WALL",
                GateStatus::NotApplicable => "N/A",
            },
            b.reason,
        )
    };
    s.push_str(&g(
        "first_order_repairable",
        &report.repairable_gate_a,
        &report.repairable_gate_b,
    ));
    s.push_str(&g(
        "kuranishi_extends",
        &report.kuranishi_gate_a,
        &report.kuranishi_gate_b,
    ));
    s.push_str(&format!("\nterminal: {}\n", report.terminal));
    s
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Print the full exact table and both invariants' gate verdicts. Run with:
    /// `cargo test -j 1 -p omega_mub print_probe_table_b -- --nocapture`.
    #[test]
    fn print_probe_table_b() {
        let report = run_probe_b();
        println!("{}", render_table_b(&report));
    }

    /// Every candidate must be an exact unit vector (norm_sq == 1) by construction.
    #[test]
    fn every_candidate_is_an_exact_unit_vector() {
        let report = run_probe_b();
        for r in &report.rows {
            assert!(
                r.is_unit,
                "candidate {} is not an exact unit vector",
                r.label
            );
        }
    }

    /// Structural invariants that must hold at every candidate: whenever a first-order repair
    /// exists it cancels the residual exactly, and whenever a Kuranishi step is computed its MC
    /// bracket is Bianchi-closed (Parseval).
    #[test]
    fn structural_invariants_hold_everywhere() {
        let report = run_probe_b();
        for r in &report.rows {
            if r.first_order_repairable {
                assert_eq!(
                    r.repair_verified,
                    Some(true),
                    "repairable candidate {} did not re-verify J.x = -omega",
                    r.label
                );
                assert_eq!(
                    r.bianchi_closed,
                    Some(true),
                    "MC bracket not Bianchi-closed at repairable candidate {}",
                    r.label
                );
                assert!(
                    r.kuranishi_extends.is_some(),
                    "repairable candidate {} missing Kuranishi verdict",
                    r.label
                );
            } else {
                assert_eq!(
                    r.kuranishi_extends, None,
                    "N/A kuranishi expected at {}",
                    r.label
                );
                assert_eq!(
                    r.repair_verified, None,
                    "N/A repair expected at {}",
                    r.label
                );
            }
        }
    }

    /// Terminal is OpenResidual — Phase-0b mints no authority.
    #[test]
    fn terminal_is_open_residual() {
        assert_eq!(run_probe_b().terminal, "OpenResidual");
    }

    // --- Observed-reality assertions (written AFTER running print_probe_table_b). ---
    // These pin the OBSERVED numbers so the verdict is replayable. They record the reality the
    // exact arithmetic produced on the first real --nocapture run, not a pre-supposed
    // expectation; if the computation ever changes they must be re-derived from a fresh table.

    use crate::omega_native::exact::d6_exact_deformation_invariance_probe::generic_unit;
    use crate::omega_native::exact::d6_exact_tangent_obstruction::REAL_DIM;

    /// OBSERVED: on the whole 14-candidate set the ACTUAL curvature is first-order obstructed
    /// everywhere (`omega(v) not in im(J)`), so the Kuranishi step is never reached, and the
    /// winding is uniformly 0.
    #[test]
    fn observed_all_candidates_first_order_obstructed() {
        let report = run_probe_b();
        for r in &report.rows {
            assert!(
                !r.first_order_repairable,
                "OBSERVED: {} must be first-order obstructed (omega not in im J)",
                r.label
            );
            assert_eq!(
                r.kuranishi_extends, None,
                "OBSERVED: kuranishi N/A at {}",
                r.label
            );
            assert_eq!(
                r.repair_verified, None,
                "OBSERVED: repair N/A at {}",
                r.label
            );
            assert_eq!(
                r.bianchi_closed, None,
                "OBSERVED: bianchi N/A at {}",
                r.label
            );
            if ["flat_ramp4", "flat_step6", "flat_step8", "flat_step12"].contains(&r.label.as_str())
            {
                assert_eq!(
                    r.degree_winding, None,
                    "OBSERVED: winding undefined (circle crosses zero, R10) at {}",
                    r.label
                );
            } else {
                assert_eq!(
                    r.degree_winding,
                    Some(0),
                    "OBSERVED: winding must be Some(0) at {}",
                    r.label
                );
            }
        }
    }

    /// OBSERVED gate verdicts. `first_order_repairable` is rigid-but-BLIND (Gate A FAIL, Gate B
    /// RIGID) — the SAME failure mode as the Phase-0 cohomological invariants, now for a
    /// curvature-seeing invariant. `kuranishi_extends` is undefined everywhere (Gate A FAIL;
    /// Gate B is NotApplicable, rejecting vacuous constancy, R09). Neither shows property (a) ∧ (b).
    #[test]
    fn observed_gate_verdicts_are_stable() {
        let report = run_probe_b();
        assert!(
            !report.repairable_gate_a.pass,
            "OBSERVED: first_order_repairable Gate A must FAIL (constant => blind to no-go)"
        );
        assert!(
            report.repairable_gate_b.pass,
            "OBSERVED: first_order_repairable Gate B RIGID (constant false across flat torus)"
        );
        assert!(report.repairable_gate_b.wall_samples.is_empty());
        assert!(
            !report.kuranishi_gate_a.pass,
            "OBSERVED: kuranishi_extends Gate A must FAIL (undefined everywhere)"
        );
        assert_eq!(
            report.kuranishi_gate_b.status,
            GateStatus::NotApplicable,
            "OBSERVED: kuranishi_extends Gate B is NotApplicable (R09)"
        );
        assert!(
            !report.kuranishi_gate_b.pass,
            "OBSERVED: kuranishi_extends Gate B rejected vacuous constancy"
        );
    }

    /// OBSERVED (fully exact): generic_unit and flat_ramp2 share the exact curvature mass 1/2,
    /// yet BOTH carry `first_order_repairable = false`. The invariant is a CONSTANT on the
    /// whole set, so it cannot track the scalar no-go (blind) even though it is trivially rigid.
    #[test]
    fn observed_exact_mass_collision_with_constant_blind_invariant() {
        let report = run_probe_b();
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
            "exact masses must coincide (1/2)"
        );
        assert!(
            !g.first_order_repairable && !f.first_order_repairable,
            "yet both carry the constant blind value false"
        );
    }

    /// Positive control: the all-`false` `first_order_repairable` column is a REAL obstruction,
    /// not a dead solver. The exact solver DOES accept an in-image target `b = J.dv0`, and DOES
    /// reject `-omega(v)` — so `false` genuinely means `omega(v) not in im(J)`.
    #[test]
    fn solver_discriminates_so_the_all_false_column_is_a_real_obstruction() {
        let cols = canonical_triple_exact();
        let v = generic_unit();
        let j = curvature_jacobian(&cols, &v);
        let mut dv0 = vec![Cyc24::zero(); REAL_DIM];
        dv0[0] = Cyc24::rat(ri(3));
        dv0[5] = Cyc24::rat(ri(1) / ri(2));
        let b = mat_vec(&j, &dv0).expect("jacobian shape");
        assert!(
            matches!(solve_exact(&j, &b), Ok(Some(_))),
            "solver must accept an in-image target b = J.dv0"
        );
        let neg_omega: Vec<Cyc24> = curvature_c2(&cols, &v).iter().map(|w| w.neg()).collect();
        assert!(
            matches!(solve_exact(&j, &neg_omega), Ok(None)),
            "-omega(generic_unit) must be first-order obstructed (not in im J)"
        );
    }
}
