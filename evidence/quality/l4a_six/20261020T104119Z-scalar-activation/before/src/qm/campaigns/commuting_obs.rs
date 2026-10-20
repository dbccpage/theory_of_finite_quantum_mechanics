use crate::qm::campaigns::causal_order::census_unlabeled;
use crate::linear_algebra::basic_matrix::BasicMatrix;
use crate::linear_algebra::{
    involution::is_hermitian,
    matrix::{commutator, is_scalar_matrix, is_zero_matrix},
};
use omega_homology::finite_poset::FinitePoset;
use omega_homology::graph_coloring::{two_coloring, TwoColoring};
use omega_lie_theory::pauli_symplectic::{pauli, Pauli};
use omega_number_theory::cyclotomic::GaussianRat;
use omega_quantum_physics::commuting_observables::*;
use serde::{Deserialize, Serialize};
use std::collections::{BTreeSet, HashMap};

pub fn construct_c1_assignment() -> Result<
    (
        HashMap<usize, BasicMatrix<GaussianRat>>,
        HashMap<usize, usize>,
    ),
    String,
> {
    let mut obs = HashMap::new();
    obs.insert(
        0,
        embed_factor_1(
            &pauli::<GaussianRat>(Pauli::X).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    );
    obs.insert(
        1,
        embed_factor_1(
            &pauli::<GaussianRat>(Pauli::Z).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    );
    obs.insert(
        2,
        embed_factor_2(
            &pauli::<GaussianRat>(Pauli::Z).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    );

    let mut factors = HashMap::new();
    factors.insert(0, 1);
    factors.insert(1, 1);
    factors.insert(2, 2);

    Ok((obs, factors))
}

pub fn construct_c2_assignment() -> Result<
    (
        HashMap<usize, BasicMatrix<GaussianRat>>,
        HashMap<usize, usize>,
    ),
    String,
> {
    let mut obs = HashMap::new();
    obs.insert(
        0,
        embed_factor_1(
            &pauli::<GaussianRat>(Pauli::X).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    );
    obs.insert(
        1,
        embed_factor_1(
            &pauli::<GaussianRat>(Pauli::Z).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    );
    obs.insert(
        2,
        embed_factor_2(
            &pauli::<GaussianRat>(Pauli::Z).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    );
    obs.insert(
        3,
        embed_factor_2(
            &pauli::<GaussianRat>(Pauli::X).expect("the exact Gaussian Pauli fixture is admitted"),
        )
        .map_err(|e| e.to_string())?,
    );

    let mut factors = HashMap::new();
    factors.insert(0, 1);
    factors.insert(1, 1);
    factors.insert(2, 2);
    factors.insert(3, 2);

    Ok((obs, factors))
}

pub fn construct_c3_antichain() -> FinitePoset {
    FinitePoset::new(3, BTreeSet::new()).unwrap()
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PosetSearchResult {
    pub poset_n: usize,
    pub strict_relations_count: usize,
    pub spacelike_pairs_count: usize,
    pub has_odd_cycle: bool,
    pub odd_cycle_witness: Option<Vec<usize>>,
    pub admitted: bool,
    pub status: String,
    pub degenerate_assignments_rejected: usize,
}

fn mask_has_monochromatic_edge(mask: usize, edges: &[(usize, usize)]) -> bool {
    for &(u, v) in edges {
        let cu = (mask >> u) & 1;
        let cv = (mask >> v) & 1;
        if cu == cv {
            return true;
        }
    }
    false
}

fn count_degenerate_assignments(n: usize, edges: &[(usize, usize)]) -> usize {
    let total_combos = 1usize << n;
    let mut rejected = 0;
    for mask in 0..total_combos {
        if mask_has_monochromatic_edge(mask, edges) {
            rejected += 1;
        }
    }
    rejected
}

fn embedded_pauli_triple(
    factor: usize,
) -> Result<[BasicMatrix<GaussianRat>; 3], String> {
    let px = pauli::<GaussianRat>(Pauli::X).expect("the exact Gaussian Pauli fixture is admitted");
    let py = pauli::<GaussianRat>(Pauli::Y).expect("the exact Gaussian Pauli fixture is admitted");
    let pz = pauli::<GaussianRat>(Pauli::Z).expect("the exact Gaussian Pauli fixture is admitted");
    if factor == 1 {
        Ok([
            embed_factor_1(&px).map_err(|e| e.to_string())?,
            embed_factor_1(&py).map_err(|e| e.to_string())?,
            embed_factor_1(&pz).map_err(|e| e.to_string())?,
        ])
    } else {
        Ok([
            embed_factor_2(&px).map_err(|e| e.to_string())?,
            embed_factor_2(&py).map_err(|e| e.to_string())?,
            embed_factor_2(&pz).map_err(|e| e.to_string())?,
        ])
    }
}

fn build_bipartite_assignment(
    n: usize,
    coloring: &[u8],
) -> Result<
    (
        HashMap<usize, BasicMatrix<GaussianRat>>,
        HashMap<usize, usize>,
    ),
    String,
> {
    let f1_ops = embedded_pauli_triple(1)?;
    let f2_ops = embedded_pauli_triple(2)?;
    let mut assignment = HashMap::new();
    let mut factor_labels = HashMap::new();
    for i in 0..n {
        let c = usize::from(coloring[i]) + 1;
        factor_labels.insert(i, c);
        let ops = if c == 1 { &f1_ops } else { &f2_ops };
        assignment.insert(i, ops[i % ops.len()].clone());
    }
    Ok((assignment, factor_labels))
}

pub fn search_poset_assignment(
    poset: &FinitePoset,
    non_degeneracy_enforced: bool,
) -> Result<PosetSearchResult, String> {
    let edges = poset.incomparable_pairs();
    if poset.size() > 20 {
        return Err("DECLARED_SEARCH_BOUND_EXCEEDED".into());
    }
    let coloring = match two_coloring(poset.size(), &edges).map_err(|e| e.to_string())? {
        TwoColoring::OddCycle(cycle) => {
            return Ok(PosetSearchResult {
                poset_n: poset.size(),
                strict_relations_count: poset.relation_count(),
                spacelike_pairs_count: edges.len(),
                has_odd_cycle: true,
                odd_cycle_witness: Some(cycle),
                admitted: false,
                status: "OBSTRUCTED_BY_ODD_CYCLE".to_string(),
                degenerate_assignments_rejected: count_degenerate_assignments(poset.size(), &edges),
            });
        }
        TwoColoring::Bipartite { colors, .. } => colors,
    };

    let (assignment, factor_labels) = build_bipartite_assignment(poset.size(), &coloring)?;
    let (valid, reason, deg_rej) =
        validate_observable_assignment(poset, &assignment, &factor_labels, non_degeneracy_enforced);

    Ok(PosetSearchResult {
        poset_n: poset.size(),
        strict_relations_count: poset.relation_count(),
        spacelike_pairs_count: edges.len(),
        has_odd_cycle: false,
        odd_cycle_witness: None,
        admitted: valid,
        status: if valid {
            "COMMUTING_ASSIGNMENT_FOUND".into()
        } else {
            reason
        },
        degenerate_assignments_rejected: deg_rej,
    })
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CensusSearchResult {
    pub posets_searched: usize,
    pub n3_census_count: usize,
    pub n3_obstructed_count: usize,
    pub n3_admitted_count: usize,
    pub n4_census_count: usize,
    pub n4_obstructed_count: usize,
    pub n4_admitted_count: usize,
    pub total_obstructed_count: usize,
    pub total_admitted_count: usize,
    pub smallest_obstructed_poset_size: Option<usize>,
    pub obstructed_poset_found: bool,
    pub odd_cycle_analysed: bool,
    pub non_degeneracy_enforced: bool,
    pub degenerate_assignments_rejected: usize,
}

pub fn search_census_at_declared_bound(
    non_degeneracy_enforced: bool,
) -> Result<CensusSearchResult, String> {
    let c3 = census_unlabeled(3).expect("three-event census is bounded");
    let c4 = census_unlabeled(4).expect("four-event census is bounded");

    let mut total_degenerate_rejected = 0;
    let mut smallest_obstructed_size = None;
    let mut obstructed_poset_found = false;

    let mut n3_obstructed = 0;
    for posets in c3.values() {
        let p = &posets[0];
        let res = search_poset_assignment(p, non_degeneracy_enforced)?;
        total_degenerate_rejected += res.degenerate_assignments_rejected;
        if !res.admitted {
            n3_obstructed += 1;
            if !obstructed_poset_found {
                obstructed_poset_found = true;
                smallest_obstructed_size = Some(3);
            }
        }
    }

    let mut n4_obstructed = 0;
    for posets in c4.values() {
        let p = &posets[0];
        let res = search_poset_assignment(p, non_degeneracy_enforced)?;
        total_degenerate_rejected += res.degenerate_assignments_rejected;
        if !res.admitted {
            n4_obstructed += 1;
            if !obstructed_poset_found {
                obstructed_poset_found = true;
                smallest_obstructed_size = Some(4);
            }
        }
    }

    Ok(CensusSearchResult {
        posets_searched: c3.len() + c4.len(),
        n3_census_count: c3.len(),
        n3_obstructed_count: n3_obstructed,
        n3_admitted_count: c3.len() - n3_obstructed,
        n4_census_count: c4.len(),
        n4_obstructed_count: n4_obstructed,
        n4_admitted_count: c4.len() - n4_obstructed,
        total_obstructed_count: n3_obstructed + n4_obstructed,
        total_admitted_count: (c3.len() - n3_obstructed) + (c4.len() - n4_obstructed),
        smallest_obstructed_poset_size: smallest_obstructed_size,
        obstructed_poset_found,
        odd_cycle_analysed: true,
        non_degeneracy_enforced,
        degenerate_assignments_rejected: total_degenerate_rejected,
    })
}

fn verify_factor_labels(n: usize, factor_labels: &HashMap<usize, usize>) -> Result<(), String> {
    for i in 0..n {
        if !matches!(factor_labels.get(&i), Some(1 | 2)) {
            return Err("observable factor is outside the declared two-factor class".into());
        }
    }
    Ok(())
}

fn collect_spacelike_pairs(
    n: usize,
    strict_set: &BTreeSet<(usize, usize)>,
) -> Vec<(usize, usize)> {
    let mut spacelike = Vec::new();
    for i in 0..n {
        for j in (i + 1)..n {
            if !strict_set.contains(&(i, j)) && !strict_set.contains(&(j, i)) {
                spacelike.push((i, j));
            }
        }
    }
    spacelike
}

fn verify_observables_hermitian_and_nonscalar(
    n: usize,
    observables: &HashMap<usize, BasicMatrix<GaussianRat>>,
    non_degeneracy_enforced: bool,
) -> Result<(), String> {
    for u in 0..n {
        let m = observables
            .get(&u)
            .ok_or_else(|| format!("Missing observable {}", u))?;
        if !is_hermitian(m).map_err(|e| e.to_string())? {
            return Err(format!("Observable {} is not Hermitian", u));
        }
        if non_degeneracy_enforced && is_scalar_matrix(m).map_err(|e| e.to_string())? {
            return Err(format!("Observable {} is scalar", u));
        }
    }
    Ok(())
}

fn verify_spacelike_commutation(
    spacelike: &[(usize, usize)],
    observables: &HashMap<usize, BasicMatrix<GaussianRat>>,
    factor_labels: &HashMap<usize, usize>,
    non_degeneracy_enforced: bool,
) -> Result<(), String> {
    for &(u, v) in spacelike {
        let m_u = observables.get(&u).unwrap();
        let m_v = observables.get(&v).unwrap();
        let comm = commutator(m_u, m_v).map_err(|e| e.to_string())?;
        if !is_zero_matrix(&comm) {
            return Err(format!("Spacelike pair ({}, {}) does not commute", u, v));
        }
        if non_degeneracy_enforced
            && factor_labels.get(&u).unwrap_or(&1) == factor_labels.get(&v).unwrap_or(&2)
        {
            return Err(format!(
                "Incomparable pair ({}, {}) shares factor and MASA",
                u, v
            ));
        }
    }
    Ok(())
}

pub fn verify_witness_independent(
    n: usize,
    strict_relations: &[(usize, usize)],
    observables: &HashMap<usize, BasicMatrix<GaussianRat>>,
    factor_labels: &HashMap<usize, usize>,
    non_degeneracy_enforced: bool,
) -> Result<bool, String> {
    if n == 0 || n > 20 {
        return Err("DECLARED_SEARCH_BOUND_EXCEEDED".into());
    }
    verify_factor_labels(n, factor_labels)?;
    let strict_set: BTreeSet<(usize, usize)> = strict_relations.iter().cloned().collect();
    FinitePoset::new(n, strict_set.clone()).map_err(|e| format!("invalid declared poset: {e}"))?;
    let spacelike = collect_spacelike_pairs(n, &strict_set);
    verify_observables_hermitian_and_nonscalar(n, observables, non_degeneracy_enforced)?;
    verify_spacelike_commutation(&spacelike, observables, factor_labels, non_degeneracy_enforced)?;
    Ok(true)
}
