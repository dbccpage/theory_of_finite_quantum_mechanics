
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

fn numeric_complex(z: &Cyc24) -> (f64, f64) {
    let mut re = 0.0f64;
    let mut im = 0.0f64;
    for (k, a) in z.a.iter().enumerate() {
        let ak = a.to_f64().unwrap_or(f64::NAN);
        let ang = std::f64::consts::PI * (k as f64) / 12.0;
        re += ak * ang.cos();
        im += ak * ang.sin();
    }
    (re, im)
}

fn numeric_re(z: &Cyc24) -> f64 {
    numeric_complex(z).0
}

fn sample_winding_angle(e6: &[(f64, f64)], vc: &[(f64, f64)], r: f64, phase: f64) -> f64 {
    let (mut are, mut aim) = (0.0f64, 0.0f64);
    for k in 0..D {
        let (vre, vim) = if k == 1 {
            (r * phase.cos(), r * phase.sin())
        } else {
            vc[k]
        };
        let (ere, eim) = e6[k];
        are += ere * vre + eim * vim;
        aim += ere * vim - eim * vre;
    }
    aim.atan2(are)
}

fn wrap_angle_delta(mut d: f64, two_pi: f64) -> f64 {
    while d > std::f64::consts::PI {
        d -= two_pi;
    }
    while d < -std::f64::consts::PI {
        d += two_pi;
    }
    d
}

fn degree_winding(columns: &[ExactVec], v: &ExactVec) -> Option<i64> {
    let mut centre = Cyc24::zero();
    for k in 0..D {
        if k != 1 {
            centre = centre.add(&columns[6][k].conj().mul(&v[k]));
        }
    }
    let amp = columns[6][1].conj().mul(&inv_sqrt6());
    if abs_sq(&centre) == abs_sq(&amp) {
        return None;
    }

    let e6: Vec<(f64, f64)> = columns[6].iter().map(numeric_complex).collect();
    let vc: Vec<(f64, f64)> = v.iter().map(numeric_complex).collect();
    let r = numeric_re(&inv_sqrt6());
    let steps = 8192usize;
    let two_pi = 2.0 * std::f64::consts::PI;
    let mut prev_ang: Option<f64> = None;
    let mut total = 0.0f64;
    for s in 0..=steps {
        let t = 24.0 * (s as f64) / (steps as f64);
        let phase = std::f64::consts::PI * t / 12.0;
        let ang = sample_winding_angle(&e6, &vc, r, phase);
        if let Some(p) = prev_ang {
            total += wrap_angle_delta(ang - p, two_pi);
        }
        prev_ang = Some(ang);
    }
    Some((total / two_pi).round() as i64)
}

#[derive(Clone, Debug)]
pub struct SampleRowB {
    pub label: String,
    pub category: SampleCategory,
    pub is_unit: bool,
    pub omega_mass_rational: Option<BigRational>,
    pub omega_mass_float: f64,
    pub omega_mass_exact: Cyc24,
    pub first_order_repairable: bool,
    pub repair_verified: Option<bool>,
    pub kuranishi_extends: Option<bool>,
    pub bianchi_closed: Option<bool>,
    pub degree_winding: Option<i64>,
}

impl SampleRowB {
    fn inv_repairable(&self) -> bool {
        self.first_order_repairable
    }
    fn inv_kuranishi(&self) -> Option<bool> {
        self.kuranishi_extends
    }
}

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

#[derive(Clone, Debug)]
pub struct GateVerdict {
    pub pass: bool,
    pub status: GateStatus,
    pub reason: String,
    pub wall_samples: Vec<String>,
    pub applicable_count: usize,
    pub total_count: usize,
}

#[derive(Clone, Debug)]
pub struct ProbeReportB {
    pub rows: Vec<SampleRowB>,
    pub repairable_gate_a: GateVerdict,
    pub repairable_gate_b: GateVerdict,
    pub kuranishi_gate_a: GateVerdict,
    pub kuranishi_gate_b: GateVerdict,
    pub terminal: &'static str,
}

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

    let j = curvature_jacobian(columns, v);
    let neg_omega: Vec<Cyc24> = omega.iter().map(|w| w.neg()).collect();
    let repair = solve_exact(&j, &neg_omega).ok().flatten();
    let first_order_repairable = repair.is_some();

    let mut repair_verified = None;
    let mut kuranishi_extends = None;
    let mut bianchi_closed = None;
    if let Some(x) = &repair {
        repair_verified = Some(mat_vec(&j, x).expect("jacobian shape") == neg_omega);
        let i = Cyc24::zeta24(6);
        let dv: ExactVec = std::array::from_fn(|k| x[2 * k].add(&i.mul(&x[2 * k + 1])));
        let so = second_order_obstruction(columns, v, &dv);
        bianchi_closed = Some(so.bianchi_closed);
        kuranishi_extends = Some(so.second_order_absorbable);
    }

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

fn is_mass_collision_pair<T: InvariantValue + PartialEq>(
    r_i: &SampleRowB,
    r_j: &SampleRowB,
    vi: &T,
    vj: &T,
) -> bool {
    vi.is_applicable()
        && vj.is_applicable()
        && r_i.omega_mass_exact == r_j.omega_mass_exact
        && vi != vj
}

fn find_mass_collision<T, F>(rows: &[SampleRowB], inv: &F) -> Option<(String, String, T, T)>
where
    T: InvariantValue + PartialEq + Clone,
    F: Fn(&SampleRowB) -> T,
{
    for i in 0..rows.len() {
        for j in (i + 1)..rows.len() {
            let vi = inv(&rows[i]);
            let vj = inv(&rows[j]);
            if is_mass_collision_pair(&rows[i], &rows[j], &vi, &vj) {
                return Some((rows[i].label.clone(), rows[j].label.clone(), vi, vj));
            }
        }
    }
    None
}

fn format_gate_a_reason<T: Debug>(
    name: &str,
    collision: &Option<(String, String, T, T)>,
    near_differs: bool,
    near_labels: &[&str],
    near_vals: &[T],
    far_vals: &[T],
) -> String {
    if let Some((li, lj, vi, vj)) = collision {
        format!(
            "EXACT decoupling: '{li}' and '{lj}' have IDENTICAL exact curvature mass yet \
             {name} = {vi:?} vs {vj:?} => sampled {name} does not factor through scalar curvature mass on this population => Gate A FAIL"
        )
    } else if !near_differs {
        format!(
            "the most-MU-like flat samples {:?} carry {name} values {:?}, all already present in \
             the far controls {:?} => flatness/MU-proximity does not move {name} => Gate A FAIL",
            near_labels, near_vals, far_vals,
        )
    } else {
        format!(
            "near-MU flat samples move {name} away from the far-control values and no exact \
             mass-collision decouples it => Gate A SIGNAL"
        )
    }
}

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

    let collision = find_mass_collision(rows, &inv);
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
    let near_labels: Vec<&str> = near.iter().map(|r| r.label.as_str()).collect();
    let reason = format_gate_a_reason(
        name,
        &collision,
        near_differs,
        &near_labels,
        &near_vals,
        &far_vals,
    );
    GateVerdict {
        pass,
        status,
        reason,
        wall_samples: Vec::new(),
        applicable_count,
        total_count,
    }
}

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

    #[test]
    fn print_probe_table_b() {
        let report = run_probe_b();
        println!("{}", render_table_b(&report));
    }

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

    #[test]
    fn terminal_is_open_residual() {
        assert_eq!(run_probe_b().terminal, "OpenResidual");
    }


    use crate::omega_native::exact::d6_exact_deformation_invariance_probe::generic_unit;
    use crate::omega_native::exact::d6_exact_tangent_obstruction::REAL_DIM;

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
