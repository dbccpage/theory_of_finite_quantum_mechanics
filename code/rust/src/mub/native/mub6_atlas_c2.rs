
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::Serialize;

use crate::native::exact::d6_exact_curvature_cochain::{canonical_triple_exact, ExactVec, D};
use crate::native::exact::mub6_cyclotomic_enclosure::{cyc24_real_imag_enclosure, SqrtBox};
use crate::native::campaign::mub6_dita_seed_cover::{
    all_genuine_dita_seeds, dita_seed_triple_columns, neighborhood_delta_1_1000,
};
use engine_kernel::interval::Interval;
#[cfg(test)]
use engine_number_theory::rational::ri;

fn abs_lower(i: &Interval) -> BigRational {
    if i.lo() >= &BigRational::zero() {
        i.lo().clone()
    } else if i.hi() <= &BigRational::zero() {
        -i.hi().clone()
    } else {
        BigRational::zero()
    }
}

fn abs_upper(i: &Interval) -> BigRational {
    let a = i.lo().abs();
    let b = i.hi().abs();
    if a >= b {
        a
    } else {
        b
    }
}

pub fn moduli_entrywise_l_inf_bounds(
    cols_a: &[ExactVec],
    cols_b: &[ExactVec],
) -> (BigRational, BigRational) {
    assert_eq!(cols_a.len(), 18);
    assert_eq!(cols_b.len(), 18);
    let sb = SqrtBox::standard();
    let mut lo = BigRational::zero();
    let mut hi = BigRational::zero();
    for ci in D..3 * D {
        for k in 0..D {
            let diff = cols_a[ci][k].sub(&cols_b[ci][k]);
            let (re, im) = cyc24_real_imag_enclosure(&diff, &sb);
            let entry_lo = abs_lower(&re).max(abs_lower(&im));
            let entry_hi = abs_upper(&re).max(abs_upper(&im));
            if entry_lo > lo {
                lo = entry_lo;
            }
            if entry_hi > hi {
                hi = entry_hi;
            }
        }
    }
    (lo, hi)
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum NeighborhoodPairRelation {
    ProvenDisjoint,
    MayOverlap,
    Inconclusive,
}

#[derive(Debug, Clone, Serialize)]
pub struct SeedPairC2 {
    pub seed_a: (i64, i64),
    pub seed_b: (i64, i64),
    pub dist_lower: String,
    pub dist_upper: String,
    pub two_delta: String,
    pub relation: NeighborhoodPairRelation,
}

#[derive(Debug, Clone, Serialize)]
pub struct T0VsDitaC2 {
    pub seed: (i64, i64),
    pub dist_lower: String,
    pub dist_upper: String,
    pub two_delta: String,
    pub relation: NeighborhoodPairRelation,
    pub note: &'static str,
}

fn pair_relation(
    lo: &BigRational,
    hi: &BigRational,
    two_delta: &BigRational,
) -> NeighborhoodPairRelation {
    if lo > two_delta {
        NeighborhoodPairRelation::ProvenDisjoint
    } else if hi <= two_delta {
        NeighborhoodPairRelation::MayOverlap
    } else {
        NeighborhoodPairRelation::Inconclusive
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct NestedContainment {
    pub seed: (i64, i64),
    pub discharged: bool,
    pub reason: &'static str,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize)]
pub enum C2Terminal {
    PartialOpenResidual,
}

#[derive(Debug, Clone, Serialize)]
pub struct AtlasC2Report {
    pub delta: String,
    pub nested: Vec<NestedContainment>,
    pub seed_pairs: Vec<SeedPairC2>,
    pub t0_vs_dita: Vec<T0VsDitaC2>,
    pub all_seed_neighborhoods_pairwise_disjoint: bool,
    pub all_nested_discharged: bool,
    pub t0_disjoint_from_all_dita_neighborhoods: bool,
    pub full_atlas_c2_discharged: bool,
    pub terminal: C2Terminal,
    pub open_obligations: Vec<&'static str>,
    pub firewall: &'static str,
}

pub fn dita_seed_atlas_c2_report() -> AtlasC2Report {
    let delta = neighborhood_delta_1_1000();
    let two_delta = &delta + &delta;
    let seeds: Vec<(i64, i64)> = all_genuine_dita_seeds()
        .into_iter()
        .map(|(dx, dy, _qa)| (dx, dy))
        .collect();
    let t0 = canonical_triple_exact();

    let nested: Vec<_> = seeds
        .iter()
        .map(|&(dx, dy)| NestedContainment {
            seed: (dx, dy),
            discharged: true,
            reason:
                "point enclosure is the δ=0 special case of widened_from_exact_columns; contained in δ=1/1000 neighborhood of the same center",
        })
        .collect();

    let mut seed_pairs = Vec::new();
    for i in 0..seeds.len() {
        for j in (i + 1)..seeds.len() {
            let (dxa, dya) = seeds[i];
            let (dxb, dyb) = seeds[j];
            let ca = dita_seed_triple_columns(dxa, dya);
            let cb = dita_seed_triple_columns(dxb, dyb);
            let (lo, hi) = moduli_entrywise_l_inf_bounds(&ca, &cb);
            let relation = pair_relation(&lo, &hi, &two_delta);
            seed_pairs.push(SeedPairC2 {
                seed_a: (dxa, dya),
                seed_b: (dxb, dyb),
                dist_lower: lo.to_string(),
                dist_upper: hi.to_string(),
                two_delta: two_delta.to_string(),
                relation,
            });
        }
    }

    let mut t0_vs_dita = Vec::new();
    for &(dx, dy) in &seeds {
        let seed_cols = dita_seed_triple_columns(dx, dy);
        let (lo, hi) = moduli_entrywise_l_inf_bounds(&t0, &seed_cols);
        let relation = pair_relation(&lo, &hi, &two_delta);
        t0_vs_dita.push(T0VsDitaC2 {
            seed: (dx, dy),
            dist_lower: lo.to_string(),
            dist_upper: hi.to_string(),
            two_delta: two_delta.to_string(),
            relation,
            note: "compares δ=1/1000 neighborhoods of T0 and of the named Dita seed",
        });
    }

    let all_seed_neighborhoods_pairwise_disjoint = seed_pairs
        .iter()
        .all(|p| p.relation == NeighborhoodPairRelation::ProvenDisjoint);
    let all_nested_discharged = nested.iter().all(|n| n.discharged);
    let t0_disjoint_from_all_dita_neighborhoods = t0_vs_dita
        .iter()
        .all(|p| p.relation == NeighborhoodPairRelation::ProvenDisjoint);

    let mut open = vec![
        "ENC-1147: union of recorded patches is not the whole moduli of MU triples",
        "basis-gluing theorem from classwise no-go to complete MUB(6) still open",
        "kernel-reflection of full 5-torus leaf boxes still open (narrow/wide cell pilots only)",
    ];
    if !all_seed_neighborhoods_pairwise_disjoint {
        open.insert(
            0,
            "some Dita neighborhood pairs may overlap — need intersection cover certificate",
        );
    }
    if !t0_disjoint_from_all_dita_neighborhoods {
        open.insert(
            0,
            "T0 neighborhood may meet some Dita neighborhood — need intersection cover for those pairs",
        );
    }

    AtlasC2Report {
        delta: delta.to_string(),
        nested,
        seed_pairs,
        t0_vs_dita,
        all_seed_neighborhoods_pairwise_disjoint,
        all_nested_discharged,
        t0_disjoint_from_all_dita_neighborhoods,
        full_atlas_c2_discharged: false,
        terminal: C2Terminal::PartialOpenResidual,
        open_obligations: open,
        firewall:
            "recorded neighborhood pairs may be pairwise disjoint without covering moduli; stated region only; mints no authority",
    }
}

pub fn write_atlas_c2_report_artifact() -> Result<std::path::PathBuf, String> {
    let report = dita_seed_atlas_c2_report();
    let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../tests/mub/artifacts");
    std::fs::create_dir_all(&dir).map_err(|e| format!("mkdir: {e}"))?;
    let path = dir.join("dita_seed_atlas_c2_report_20260724.json");
    let json = serde_json::to_string_pretty(&report).map_err(|e| format!("ser: {e}"))?;
    std::fs::write(&path, json).map_err(|e| format!("write: {e}"))?;
    Ok(path)
}


#[derive(Debug, Clone, Serialize)]
pub struct KernelReflectionPilot {
    pub schema_version: &'static str,
    pub seed: (i64, i64),
    pub region: &'static str,
    pub cover: crate::native::exact::mub6_cover_run::CoverCertificate,
    pub lean_consume_target: &'static str,
    pub held_out_claim: &'static str,
    pub firewall: &'static str,
}

pub fn kernel_reflection_pilot_dita_0_8_narrow() -> KernelReflectionPilot {
    use crate::native::campaign::mub6_dita_seed_cover::{cover_seed_region, narrow_torus_cell};
    let cover = cover_seed_region(0, 8, narrow_torus_cell(), 24);
    KernelReflectionPilot {
        schema_version: "omega.mub.kernel-reflection-pilot.v1",
        seed: (0, 8),
        region: "narrow_torus_cell (stated region; not full 5-torus)",
        cover,
        lean_consume_target: "MUB.FiniteVectorCover.no_mu_vector_in_cover / MUB.KernelReflectionPilot",
        held_out_claim:
            "complete stated-region cover of the narrow torus cell against the fixed seed triple; min_gap > 0 is the exact positivity witness for every leaf in that region",
        firewall:
            "pilot region only; not full 5-torus reflection; stated region only; mints no authority",
    }
}

pub fn kernel_reflection_pilot_dita_0_8_wide() -> KernelReflectionPilot {
    use crate::native::campaign::mub6_dita_seed_cover::{
        cover_seed_region_prefiltered, wide_torus_cell,
    };
    let cover = cover_seed_region_prefiltered(0, 8, wide_torus_cell(), 30);
    KernelReflectionPilot {
        schema_version: "omega.mub.kernel-reflection-pilot.v1",
        seed: (0, 8),
        region: "wide_torus_cell (stated region; not full 5-torus)",
        cover,
        lean_consume_target: "MUB.FiniteVectorCover.no_mu_vector_in_cover / MUB.KernelReflectionPilot",
        held_out_claim:
            "complete stated-region prefiltered cover of the wide torus cell; min_gap > 0 witnesses leaf positivity",
        firewall:
            "wide-cell pilot only; not full 5-torus reflection; stated region only; mints no authority",
    }
}

fn write_pilot(
    path_name: &str,
    pilot: &KernelReflectionPilot,
) -> Result<std::path::PathBuf, String> {
    if !pilot.cover.complete || pilot.cover.uncertified != 0 {
        return Err(format!(
            "refusing incomplete pilot {path_name}: complete={} uncertified={}",
            pilot.cover.complete, pilot.cover.uncertified
        ));
    }
    let dir = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../../tests/mub/artifacts");
    std::fs::create_dir_all(&dir).map_err(|e| format!("mkdir: {e}"))?;
    let path = dir.join(path_name);
    let json = serde_json::to_string_pretty(pilot).map_err(|e| format!("ser: {e}"))?;
    std::fs::write(&path, json).map_err(|e| format!("write: {e}"))?;
    Ok(path)
}

pub fn write_kernel_reflection_pilot_artifact() -> Result<std::path::PathBuf, String> {
    write_pilot(
        "kernel_reflection_pilot_dita_0_8_narrow_cell.json",
        &kernel_reflection_pilot_dita_0_8_narrow(),
    )
}

pub fn write_kernel_reflection_wide_pilot_artifact() -> Result<std::path::PathBuf, String> {
    write_pilot(
        "kernel_reflection_pilot_dita_0_8_wide_cell.json",
        &kernel_reflection_pilot_dita_0_8_wide(),
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn nested_containment_discharged_for_all_seeds() {
        let r = dita_seed_atlas_c2_report();
        assert!(r.all_nested_discharged);
        assert_eq!(r.nested.len(), 6);
        assert!(!r.full_atlas_c2_discharged);
        assert_eq!(r.terminal, C2Terminal::PartialOpenResidual);
        assert!(r.firewall.contains("mints no authority"));
    }

    #[test]
    fn seed_pair_distances_are_exact_and_self_consistent() {
        let r = dita_seed_atlas_c2_report();
        assert_eq!(r.seed_pairs.len(), 15);
        let two_delta = ri(1) / ri(500);
        for p in &r.seed_pairs {
            let lo: BigRational = p.dist_lower.parse().unwrap();
            let hi: BigRational = p.dist_upper.parse().unwrap();
            assert!(lo <= hi, "lower ≤ upper for {:?}", p.seed_a);
            assert!(lo >= BigRational::zero());
            assert!(
                hi > BigRational::zero(),
                "distinct seeds must have positive distance upper bound"
            );
            match p.relation {
                NeighborhoodPairRelation::ProvenDisjoint => assert!(lo > two_delta),
                NeighborhoodPairRelation::MayOverlap => assert!(hi <= two_delta),
                NeighborhoodPairRelation::Inconclusive => {
                    assert!(lo <= two_delta && hi > two_delta);
                }
            }
        }
    }

    #[test]
    fn t0_vs_dita_distances_charted() {
        let r = dita_seed_atlas_c2_report();
        assert_eq!(r.t0_vs_dita.len(), 6);
        let two_delta = ri(1) / ri(500);
        for p in &r.t0_vs_dita {
            let lo: BigRational = p.dist_lower.parse().unwrap();
            let hi: BigRational = p.dist_upper.parse().unwrap();
            assert!(lo <= hi);
            assert!(
                hi > BigRational::zero(),
                "T0 must differ from Dita seed {:?}",
                p.seed
            );
            match p.relation {
                NeighborhoodPairRelation::ProvenDisjoint => assert!(lo > two_delta),
                NeighborhoodPairRelation::MayOverlap => assert!(hi <= two_delta),
                NeighborhoodPairRelation::Inconclusive => {
                    assert!(lo <= two_delta && hi > two_delta);
                }
            }
        }
        assert_eq!(
            r.t0_disjoint_from_all_dita_neighborhoods,
            r.t0_vs_dita
                .iter()
                .all(|p| p.relation == NeighborhoodPairRelation::ProvenDisjoint)
        );
    }

    #[test]
    fn kernel_reflection_pilot_is_complete_stated_region() {
        let p = kernel_reflection_pilot_dita_0_8_narrow();
        assert!(p.cover.complete);
        assert_eq!(p.cover.uncertified, 0);
        assert!(p.cover.certified >= 1);
        assert!(p.cover.min_gap.is_some());
        let gap: BigRational = p.cover.min_gap.as_ref().unwrap().parse().unwrap();
        assert!(gap > BigRational::zero());
        assert!(p.firewall.contains("mints no authority"));
    }

    #[test]
    fn kernel_reflection_wide_pilot_is_complete_stated_region() {
        let p = kernel_reflection_pilot_dita_0_8_wide();
        assert!(p.cover.complete);
        assert_eq!(p.cover.uncertified, 0);
        assert!(p.cover.certified >= 1);
        assert!(p.cover.min_gap.is_some());
        let gap: BigRational = p.cover.min_gap.as_ref().unwrap().parse().unwrap();
        assert!(gap > BigRational::zero());
    }

    #[test]
    fn write_c2_and_pilot_artifacts() {
        let c2 = write_atlas_c2_report_artifact().expect("write c2");
        assert!(c2.exists());
        let pilot = write_kernel_reflection_pilot_artifact().expect("write pilot");
        assert!(pilot.exists());
        let wide = write_kernel_reflection_wide_pilot_artifact().expect("write wide");
        assert!(wide.exists());
    }
}
