
use num_rational::BigRational;
use num_traits::ToPrimitive;

use crate::native::exact::d6_exact_curvature_cochain::{
    abs_sq, as_rational, canonical_triple_exact, cmp_exact_real, curvature_c2, norm_sq,
    wall_functional, ExactVec,
};
use crate::native::exact::d6_exact_obstruction_cohomology::obstruction_cohomology;
use crate::native::exact::d6_exact_tangent_obstruction::tangent_obstruction;
use tfqm_number_theory::cyclotomic::Cyc24;
use tfqm_number_theory::rational::ri;

crate::fixture_set!(fixtures, "d6_exact_deformation_invariance_probe");

fn rat(num: i64, den: i64) -> Cyc24 {
    Cyc24::rat(ri(num) / ri(den))
}

pub(crate) use crate::native::exact::mub6_field::inv_sqrt6;

fn zero_vec() -> ExactVec {
    std::array::from_fn(|_| Cyc24::zero())
}

pub(crate) fn unit_e0() -> ExactVec {
    let mut v = zero_vec();
    v[0] = Cyc24::rat(ri(1));
    v
}

pub(crate) fn generic_unit() -> ExactVec {
    let s = Cyc24::sqrt2().mul(&rat(1, 2));
    let mut v = zero_vec();
    v[0] = s.clone();
    v[1] = Cyc24::zeta24(6).mul(&s);
    v
}

pub(crate) fn flat_candidate(exps: [i64; 6]) -> ExactVec {
    let s = inv_sqrt6();
    std::array::from_fn(|k| s.mul(&Cyc24::zeta24(exps[k] as i32)))
}

pub(crate) fn numeric_re(z: &Cyc24) -> f64 {
    let mut acc = 0.0f64;
    for (k, a) in z.a.iter().enumerate() {
        let ak = a.to_f64().unwrap_or(f64::NAN);
        acc += ak * (std::f64::consts::PI * (k as f64) / 12.0).cos();
    }
    acc
}

#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Debug)]
pub enum SampleCategory {
    FarControl,
    FlatTorus,
}

#[derive(Clone, Debug)]
pub struct SampleRow {
    pub label: String,
    pub category: SampleCategory,
    pub is_unit: bool,
    pub f_rational: Option<BigRational>,
    pub f_float: f64,
    pub omega_mass_rational: Option<BigRational>,
    pub omega_mass_float: f64,
    pub omega_mass_exact: Cyc24,
    pub rank_j: usize,
    pub coker_dim: usize,
    pub h1_dim: Option<usize>,
    pub h2_dim: usize,
    pub phase_gauge_in_kernel: bool,
    pub d1_after_d0_zero: bool,
}

impl SampleRow {
    pub fn invariant_pair(&self) -> (usize, Option<usize>) {
        (self.rank_j, self.h1_dim)
    }
}

#[derive(Clone, Debug)]
pub struct ProbeReport {
    pub rows: Vec<SampleRow>,
    pub gate_a_pass: bool,
    pub gate_a_reason: String,
    pub gate_b_pass: bool,
    pub gate_b_reason: String,
    pub wall_samples: Vec<String>,
    pub terminal: &'static str,
}

pub(crate) fn candidate_set() -> Vec<(String, SampleCategory, ExactVec)> {
    let mut set: Vec<(String, SampleCategory, ExactVec)> = Vec::new();

    set.push(("e_0".to_string(), SampleCategory::FarControl, unit_e0()));
    set.push((
        "generic_unit".to_string(),
        SampleCategory::FarControl,
        generic_unit(),
    ));

    let tuples: [(&str, [i64; 6]); 12] = [
        ("flat_zeros", [0, 0, 0, 0, 0, 0]),
        ("flat_ramp1", [0, 1, 2, 3, 4, 5]),
        ("flat_ramp2", [0, 2, 4, 6, 8, 10]),
        ("flat_ramp3", [0, 3, 6, 9, 12, 15]),
        ("flat_ramp4", [0, 4, 8, 12, 16, 20]),
        ("flat_ramp5", [0, 5, 10, 15, 20, 1]),
        ("flat_quad_sq", [0, 1, 4, 9, 16, 1]),
        ("flat_tri", [0, 1, 3, 6, 10, 15]),
        ("flat_step6", [0, 6, 12, 18, 0, 6]),
        ("flat_step8", [0, 8, 16, 0, 8, 16]),
        ("flat_step12", [0, 12, 0, 12, 0, 12]),
        ("flat_quad_ii", [0, 2, 6, 12, 20, 6]),
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

fn compute_row(
    columns: &[ExactVec],
    label: &str,
    category: SampleCategory,
    v: &ExactVec,
) -> SampleRow {
    let is_unit = norm_sq(v) == Cyc24::rat(ri(1));

    let omega = curvature_c2(columns, v);

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

pub fn run_probe() -> ProbeReport {
    run_probe_on_columns(&canonical_triple_exact())
}

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
    let mut flat_by_mass: Vec<&SampleRow> = flat_rows.clone();
    flat_by_mass.sort_by(|a, b| cmp_exact_real(&a.omega_mass_exact, &b.omega_mass_exact));
    let near_mu_count = (flat_by_mass.len() / 3).max(1);
    let near_mu: Vec<&SampleRow> = flat_by_mass.iter().take(near_mu_count).copied().collect();
    let near_mu_pairs: Vec<(usize, Option<usize>)> =
        near_mu.iter().map(|r| r.invariant_pair()).collect();
    let near_mu_differs_from_far = near_mu_pairs.iter().any(|p| !far_pairs.contains(p));

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

fn fmt_rat(r: &Option<BigRational>) -> String {
    match r {
        Some(q) => format!("{}", q),
        None => "non-rational-cyclotomic".to_string(),
    }
}

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

    #[test]
    fn print_probe_table() {
        let report = run_probe();
        println!("{}", render_table(&report));
    }

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
            assert_eq!(
                r.rank_j + r.coker_dim,
                super::super::d6_exact_curvature_cochain::COLUMN_COUNT
            );
            assert_eq!(r.h1_dim.map(|h| h + 2), Some(r.coker_dim));
        }
    }

    #[test]
    fn flat_candidates_have_exact_sixth_modulus() {
        use crate::native::exact::d6_exact_curvature_cochain::D;
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

    #[test]
    fn terminal_is_open_residual() {
        assert_eq!(run_probe().terminal, "OpenResidual");
    }


    #[test]
    fn observed_gate_verdicts_are_stable() {
        let report = run_probe();
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
        assert!(report.rows.iter().all(|r| r.h1_dim.is_some_and(|h| h >= 5)));
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
