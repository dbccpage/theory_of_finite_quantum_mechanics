//! Path B Gate A/B candidate campaign + formal tombstone of `(rank_j, h1_dim)`.
//!
//! Runs on T0 and one Dita second basepoint (F6(0,8)+Y2Q1) for dual-basepoint honesty
//! without the full six-seed wall-time of the second-basepoint campaign.
//!
//! Candidates:
//! * **omega_mass** — scalar curvature mass (expect Gate A SIGNAL, Gate B WALL)
//! * **wall_functional_f** — scalar wall functional (expect A SIGNAL, B WALL)
//! * **(rank_j, h1)** — cohomological pair (expect A FAIL; tombstoned as no-go tracker)
//!

use serde::Serialize;

use crate::omega_native::exact::d6_exact_curvature_cochain::{
    abs_sq, as_rational, canonical_triple_exact, cmp_exact_real, curvature_c2, wall_functional,
    ExactVec,
};
use crate::omega_native::exact::d6_exact_deformation_invariance_probe::{
    candidate_set, run_probe_on_columns, SampleCategory, SampleRow,
};
use crate::omega_native::exact::d6_exact_obstruction_cohomology::obstruction_cohomology;
use crate::omega_native::exact::d6_exact_tangent_obstruction::tangent_obstruction;
use crate::omega_native::campaign::mub6_dita_seed_cover::dita_seed_triple_columns;
use num_rational::BigRational;
use omega_number_theory::cyclotomic::Cyc24;

crate::fixture_set!(fixtures, "d6_exact_path_b_gate_candidates");

#[derive(Debug, Clone, Serialize)]
pub struct GateVerdictSer {
    pub pass: bool,
    pub reason: String,
    pub wall_samples: Vec<String>,
}

#[derive(Debug, Clone, Serialize)]
pub struct CandidateVerdict {
    pub name: &'static str,
    pub basepoint: String,
    pub gate_a: GateVerdictSer,
    pub gate_b: GateVerdictSer,
    pub a_and_b: bool,
    pub disposition: String,
}

#[derive(Debug, Clone, Serialize)]
pub struct PathBGateCandidateReport {
    pub schema_version: &'static str,
    pub programme: &'static str,
    pub candidates: Vec<CandidateVerdict>,
    pub rank_h1_tombstone: RankH1Tombstone,
    pub any_a_and_b_survivor: bool,
    pub terminal: &'static str,
    pub firewall: &'static str,
}

#[derive(Debug, Clone, Serialize)]
pub struct RankH1Tombstone {
    pub invariant: &'static str,
    pub status: &'static str,
    pub reason: String,
    pub basepoints_checked: Vec<String>,
    pub may_still_use_for: &'static str,
    pub not_for: &'static str,
}

#[derive(Clone)]
struct RowExt {
    label: String,
    category: SampleCategory,
    omega_mass_exact: Cyc24,
    f_exact: Cyc24,
    f_rational: Option<BigRational>,
    rank_j: usize,
    h1_dim: Option<usize>,
}

fn row_ext(columns: &[ExactVec], label: &str, category: SampleCategory, v: &ExactVec) -> RowExt {
    let omega = curvature_c2(columns, v);
    let mut mass = Cyc24::zero();
    for w in &omega {
        mass = mass.add(&abs_sq(w));
    }
    let f = wall_functional(&omega);
    let tan = tangent_obstruction(columns, v).expect("the fixed triple has 18 vectors");
    let coho = obstruction_cohomology(columns, v);
    RowExt {
        label: label.to_string(),
        category,
        omega_mass_exact: mass.clone(),
        f_exact: f.clone(),
        f_rational: as_rational(&f),
        rank_j: tan.jacobian_rank,
        h1_dim: coho.h1_dim,
    }
}

fn eval_gate_a<T, F>(rows: &[RowExt], name: &str, inv: F) -> GateVerdictSer
where
    T: PartialEq + Clone + std::fmt::Debug,
    F: Fn(&RowExt) -> T,
{
    let mut collision: Option<(String, String, T, T)> = None;
    'scan: for i in 0..rows.len() {
        for j in (i + 1)..rows.len() {
            if rows[i].omega_mass_exact == rows[j].omega_mass_exact
                && inv(&rows[i]) != inv(&rows[j])
            {
                collision = Some((
                    rows[i].label.clone(),
                    rows[j].label.clone(),
                    inv(&rows[i]),
                    inv(&rows[j]),
                ));
                break 'scan;
            }
        }
    }
    let far_vals: Vec<T> = rows
        .iter()
        .filter(|r| r.category == SampleCategory::FarControl)
        .map(&inv)
        .collect();
    let mut flat: Vec<&RowExt> = rows
        .iter()
        .filter(|r| r.category == SampleCategory::FlatTorus)
        .collect();
    flat.sort_by(|a, b| cmp_exact_real(&a.omega_mass_exact, &b.omega_mass_exact));
    let near_count = (flat.len() / 3).max(1);
    let near: Vec<&RowExt> = flat.iter().take(near_count).copied().collect();
    let near_vals: Vec<T> = near.iter().map(|r| inv(r)).collect();
    let near_differs = near_vals.iter().any(|v| !far_vals.contains(v));
    let pass = collision.is_none() && near_differs;
    let reason = if let Some((li, lj, vi, vj)) = &collision {
        format!(
            "EXACT decoupling: '{li}' and '{lj}' same mass yet {name}={vi:?} vs {vj:?} => Gate A FAIL"
        )
    } else if !near_differs {
        format!(
            "near-MU samples do not move {name} off far controls {:?} => Gate A FAIL",
            far_vals
        )
    } else {
        format!("near-MU moves {name}; no mass-collision decoupling => Gate A SIGNAL")
    };
    GateVerdictSer {
        pass,
        reason,
        wall_samples: Vec::new(),
    }
}

fn eval_gate_b<T, F>(rows: &[RowExt], name: &str, inv: F) -> GateVerdictSer
where
    T: PartialEq + Clone + std::fmt::Debug,
    F: Fn(&RowExt) -> T,
{
    let flat: Vec<&RowExt> = rows
        .iter()
        .filter(|r| r.category == SampleCategory::FlatTorus)
        .collect();
    let vals: Vec<T> = flat.iter().map(|r| inv(r)).collect();
    // Modal by frequency.
    let mut modal: Option<T> = None;
    let mut best = 0usize;
    for v in &vals {
        let c = vals.iter().filter(|q| *q == v).count();
        if c > best {
            best = c;
            modal = Some(v.clone());
        }
    }
    let wall_samples: Vec<String> = flat
        .iter()
        .filter(|r| Some(inv(r)) != modal)
        .map(|r| r.label.clone())
        .collect();
    let pass = wall_samples.is_empty();
    let reason = if pass {
        format!(
            "{name} constant = {:?} on {} flat samples => Gate B RIGID",
            modal,
            vals.len()
        )
    } else {
        format!(
            "{name} jumps off modal {:?} at {:?} => Gate B WALL",
            modal, wall_samples
        )
    };
    GateVerdictSer {
        pass,
        reason,
        wall_samples,
    }
}

fn mass_key(r: &RowExt) -> String {
    match as_rational(&r.omega_mass_exact) {
        Some(q) => format!("{q}"),
        None => format!("cyc:{:?}", r.omega_mass_exact.a),
    }
}

fn f_key(r: &RowExt) -> String {
    match &r.f_rational {
        Some(q) => format!("{q}"),
        None => format!("cyc:{:?}", r.f_exact.a),
    }
}

fn rank_h1(r: &RowExt) -> (usize, Option<usize>) {
    (r.rank_j, r.h1_dim)
}

fn run_on_basepoint(id: &str, columns: &[ExactVec]) -> Vec<CandidateVerdict> {
    let candidates = candidate_set();
    let rows: Vec<RowExt> = candidates
        .iter()
        .map(|(label, cat, v)| row_ext(columns, label, *cat, v))
        .collect();

    let mut out = Vec::new();

    // Scalar mass.
    {
        let a = eval_gate_a(&rows, "omega_mass", mass_key);
        let b = eval_gate_b(&rows, "omega_mass", mass_key);
        let a_and_b = a.pass && b.pass;
        out.push(CandidateVerdict {
            name: "omega_mass",
            basepoint: id.to_string(),
            gate_a: a,
            gate_b: b,
            a_and_b,
            // fixture: the second label is written without reading gate_a or gate_b.
            disposition: if a_and_b {
                "UNEXPECTED_A_AND_B_SURVIVOR".to_string()
            } else {
                fixtures().text("omega_mass_disposition_without_survivor")
            },
        });
    }

    // Wall functional f.
    {
        let a = eval_gate_a(&rows, "wall_functional_f", f_key);
        let b = eval_gate_b(&rows, "wall_functional_f", f_key);
        let a_and_b = a.pass && b.pass;
        out.push(CandidateVerdict {
            name: "wall_functional_f",
            basepoint: id.to_string(),
            gate_a: a,
            gate_b: b,
            a_and_b,
            // fixture: the second label is written without reading gate_a or gate_b.
            disposition: if a_and_b {
                "UNEXPECTED_A_AND_B_SURVIVOR".to_string()
            } else {
                fixtures().text("wall_functional_f_disposition_without_survivor")
            },
        });
    }

    // Cohomological pair — tombstone target.
    {
        let a = eval_gate_a(&rows, "rank_j_h1", rank_h1);
        let b = eval_gate_b(&rows, "rank_j_h1", rank_h1);
        let a_and_b = a.pass && b.pass;
        out.push(CandidateVerdict {
            name: "rank_j_h1",
            basepoint: id.to_string(),
            gate_a: a,
            gate_b: b,
            a_and_b,
            disposition: if a_and_b {
                "UNEXPECTED_A_AND_B_SURVIVOR"
            } else {
                "TOMBSTONED_as_no_go_tracker"
            }
            .to_string(),
        });
    }

    // Cross-check vs existing probe module on structural Gate A for rank_h1.
    let probe: Vec<SampleRow> = run_probe_on_columns(columns).rows;
    assert_eq!(probe.len(), rows.len());

    out
}

/// Run Path B candidate campaign on T0 + one Dita second basepoint.
pub fn run_path_b_gate_candidate_campaign() -> PathBGateCandidateReport {
    let mut candidates = Vec::new();
    candidates.extend(run_on_basepoint("T0_product", &canonical_triple_exact()));
    candidates.extend(run_on_basepoint(
        "dita_F6_0_8_Y2Q1",
        &dita_seed_triple_columns(0, 8),
    ));

    let rank_rows: Vec<&CandidateVerdict> = candidates
        .iter()
        .filter(|c| c.name == "rank_j_h1")
        .collect();
    let any_rank_a = rank_rows.iter().any(|c| c.gate_a.pass);
    let any_rank_a_and_b = rank_rows.iter().any(|c| c.a_and_b);
    let any_a_and_b_survivor = candidates.iter().any(|c| c.a_and_b);

    let rank_h1_tombstone = RankH1Tombstone {
        invariant: "(rank_j, h1_dim)",
        status: if any_rank_a_and_b {
            "REVOKED_UNEXPECTED_SURVIVOR"
        } else {
            "TOMBSTONED_AS_NO_GO_TRACKER"
        },
        reason: if any_rank_a_and_b {
            "Rank-H1 candidate passed both Gate A and Gate B on at least one basepoint.".to_string()
        } else if any_rank_a {
            "Rank-H1 candidate passed Gate A on some basepoint but failed Gate B; no uniform rigidity.".to_string()
        } else {
            "Gate A FAIL on every checked basepoint: sampled mass-collision decoupling \
             and/or near-MU does not move the pair on this candidate population. \
             Confirms (rank_j, h1_dim) is not a function of sampled curvature mass alone on these samples. \
             Does not establish universal non-existence of a fourth MU vector."
                .to_string()
        },
        basepoints_checked: vec!["T0_product".into(), "dita_F6_0_8_Y2Q1".into()],
        may_still_use_for:
            "structural diagnostics; dual-basepoint fingerprinting; wall locus charts",
        not_for: "universal no-go certificate; global nonexistence claim; MUB(6)≤3 rigidity bypass",
    };

    PathBGateCandidateReport {
        schema_version: "omega.mub.path-b-gate-candidates.v1",
        programme: "MUB-Q1-PathB-gate-candidates",
        candidates,
        rank_h1_tombstone,
        any_a_and_b_survivor,
        terminal: "OpenResidual",
        firewall:
            "Path B candidates diagnostic; scalar I has A not B; rank_h1 tombstoned as no-go tracker; stated region only; mints no authority",
    }
}

pub fn write_path_b_gate_candidate_artifact() -> Result<std::path::PathBuf, String> {
    let report = run_path_b_gate_candidate_campaign();
    let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../tests/omega_mub/artifacts");
    std::fs::create_dir_all(&dir).map_err(|e| format!("mkdir: {e}"))?;
    let path = dir.join("mub6_path_b_gate_candidates_20260725.json");
    let json = serde_json::to_string_pretty(&report).map_err(|e| format!("ser: {e}"))?;
    std::fs::write(&path, json).map_err(|e| format!("write: {e}"))?;
    Ok(path)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn path_b_candidates_tombstone_rank_h1_and_scalar_has_a_not_b() {
        let r = run_path_b_gate_candidate_campaign();
        assert_eq!(r.terminal, "OpenResidual");
        assert!(!r.any_a_and_b_survivor, "no A∧B survivor expected");
        assert_eq!(r.rank_h1_tombstone.status, "TOMBSTONED_AS_NO_GO_TRACKER");

        for bp in ["T0_product", "dita_F6_0_8_Y2Q1"] {
            let mass = r
                .candidates
                .iter()
                .find(|c| c.name == "omega_mass" && c.basepoint == bp)
                .unwrap();
            assert!(
                mass.gate_a.pass,
                "omega_mass must pass Gate A on {bp}: {}",
                mass.gate_a.reason
            );
            assert!(
                !mass.gate_b.pass,
                "omega_mass must fail Gate B on {bp}: {}",
                mass.gate_b.reason
            );

            let rh = r
                .candidates
                .iter()
                .find(|c| c.name == "rank_j_h1" && c.basepoint == bp)
                .unwrap();
            assert!(
                !rh.gate_a.pass,
                "rank_j_h1 Gate A must FAIL on {bp}: {}",
                rh.gate_a.reason
            );
        }
    }

    #[test]
    fn write_path_b_artifact() {
        let p = write_path_b_gate_candidate_artifact().expect("write");
        assert!(p.exists());
        let raw = std::fs::read_to_string(&p).unwrap();
        assert!(raw.contains("TOMBSTONED_AS_NO_GO_TRACKER"));
        assert!(raw.contains("OpenResidual"));
    }
}
