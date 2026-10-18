//! Generalized Inverted Index (GIN) Engine for Fermion Modes, Involution Doublet Cancellation,
//! and Kitaev Chain Majorana Zero Mode Decoupling.
//!
//! AuthorityEffect: None.

#![forbid(unsafe_code)]

use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct FermionConfiguration {
    pub cfg_id: u64,
    pub model_name: String,
    pub occupied_modes: BTreeSet<usize>,
    pub total_modes: usize,
    pub weight: BigRational,
    pub jw_sign: i64,
    pub parity_sector: i64,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct InvolutionCancellationReceipt {
    pub model_name: String,
    pub pairs_audited: usize,
    pub all_exact_cancellations: bool,
    pub max_weight_defect: BigRational,
    pub total_uncancelled_mass: BigRational,
    pub terminal_route: String,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct MajoranaZeroModeReceipt {
    pub chain_length_l: usize,
    pub total_modes_audited: usize,
    pub unpaired_zero_modes: Vec<usize>,
    pub bulk_bonded_modes: Vec<usize>,
    pub is_boundary_isolated: bool,
    pub mzm_status: String,
}

/// Inverted posting list index mapping fermion orbital modes to many-body configuration IDs.
#[derive(Clone, Debug, Default)]
pub struct GinIndex {
    pub configurations: BTreeMap<u64, FermionConfiguration>,
    /// Posting lists: mode_id -> set of cfg_ids where mode is occupied
    pub posting_lists: BTreeMap<usize, BTreeSet<u64>>,
}

impl GinIndex {
    pub fn new() -> Self {
        Self::default()
    }

    /// Index a configuration and populate mode posting lists.
    pub fn index_configuration(
        &mut self,
        cfg_id: u64,
        model_name: impl Into<String>,
        occupied_modes: BTreeSet<usize>,
        total_modes: usize,
        weight: BigRational,
        jw_sign: i64,
        parity_sector: i64,
    ) {
        for &m in &occupied_modes {
            self.posting_lists.entry(m).or_default().insert(cfg_id);
        }
        self.configurations.insert(
            cfg_id,
            FermionConfiguration {
                cfg_id,
                model_name: model_name.into(),
                occupied_modes,
                total_modes,
                weight,
                jw_sign,
                parity_sector,
            },
        );
    }

    /// Fast inverted posting list query: intersection of required modes minus forbidden modes.
    pub fn query_by_modes(
        &self,
        required_modes: &BTreeSet<usize>,
        forbidden_modes: &BTreeSet<usize>,
    ) -> BTreeSet<u64> {
        let mut candidates: BTreeSet<u64> = if required_modes.is_empty() {
            self.configurations.keys().copied().collect()
        } else {
            let mut iter = required_modes.iter();
            let first_mode = iter.next().unwrap();
            let mut set = self
                .posting_lists
                .get(first_mode)
                .cloned()
                .unwrap_or_default();
            for m in iter {
                if let Some(posting) = self.posting_lists.get(m) {
                    set.retain(|id| posting.contains(id));
                } else {
                    return BTreeSet::new();
                }
            }
            set
        };

        for m in forbidden_modes {
            if let Some(posting) = self.posting_lists.get(m) {
                candidates.retain(|id| !posting.contains(id));
            }
        }
        candidates
    }

    /// Find unique involution partner differing exactly on flip_modes.
    pub fn find_involution_partner(
        &self,
        cfg_id: u64,
        flip_modes: &BTreeSet<usize>,
        total_modes: usize,
    ) -> Option<u64> {
        let current = self.configurations.get(&cfg_id)?;

        let mut required = BTreeSet::new();
        let mut forbidden = BTreeSet::new();

        for m in 1..=total_modes {
            let cur_occ = current.occupied_modes.contains(&m);
            let flipped = flip_modes.contains(&m);
            let target_occ = cur_occ ^ flipped;
            if target_occ {
                required.insert(m);
            } else {
                forbidden.insert(m);
            }
        }

        let mut candidates = self.query_by_modes(&required, &forbidden);
        candidates.remove(&cfg_id);
        candidates.into_iter().next()
    }

    /// Audit a collection of involution pairs for exact opposite-sign and identical-weight cancellation.
    pub fn audit_involution_cancellations(
        &self,
        model_name: &str,
        pairs: &[(u64, u64)],
    ) -> InvolutionCancellationReceipt {
        let mut max_defect = BigRational::zero();
        let mut total_uncancelled = BigRational::zero();
        let mut all_exact = !pairs.is_empty();

        for &(id_a, id_b) in pairs {
            let (cfg_a, cfg_b) = match (self.configurations.get(&id_a), self.configurations.get(&id_b)) {
                (Some(a), Some(b)) => (a, b),
                _ => {
                    all_exact = false;
                    continue;
                }
            };

            let opposite_sign = cfg_a.jw_sign == -cfg_b.jw_sign;
            let weight_diff = (&cfg_a.weight - &cfg_b.weight).abs();

            if weight_diff > max_defect {
                max_defect = weight_diff.clone();
            }

            if !opposite_sign || !weight_diff.is_zero() {
                all_exact = false;
                total_uncancelled = total_uncancelled + weight_diff;
            }
        }

        let terminal_route = if all_exact {
            "ExactRepair".to_string()
        } else {
            "OpenSignObstruction".to_string()
        };

        InvolutionCancellationReceipt {
            model_name: model_name.to_string(),
            pairs_audited: pairs.len(),
            all_exact_cancellations: all_exact,
            max_weight_defect: max_defect,
            total_uncancelled_mass: total_uncancelled,
            terminal_route,
        }
    }
}

/// Audit 1D Kitaev chain Majorana zero modes at sweet-spot chemical potential.
/// Chain length L has 2L Majorana operators \gamma_1, ..., \gamma_{2L}.
/// Bulk sweet-spot bonds are (\gamma_{2j}, \gamma_{2j+1}) for j = 1, ..., L-1.
/// Unpaired boundary modes are \gamma_1 and \gamma_{2L}.
pub fn audit_kitaev_chain_majorana(l: usize) -> Result<MajoranaZeroModeReceipt, &'static str> {
    if l < 2 {
        return Err("Kitaev chain requires at least 2 lattice sites (L >= 2)");
    }
    let total_modes = 2 * l;
    let mut bulk_bonds = Vec::new();
    let mut bulk_modes_set = BTreeSet::new();

    for j in 1..l {
        let u = 2 * j;
        let v = 2 * j + 1;
        bulk_bonds.push((u, v));
        bulk_modes_set.insert(u);
        bulk_modes_set.insert(v);
    }

    let edge_modes = vec![1, total_modes];
    let mut is_boundary_isolated = true;

    for &edge in &edge_modes {
        if bulk_modes_set.contains(&edge) {
            is_boundary_isolated = false;
        }
    }

    let bulk_bonded_modes: Vec<usize> = bulk_modes_set.into_iter().collect();
    let mzm_status = if is_boundary_isolated && bulk_bonded_modes.len() == total_modes - 2 {
        "MZM_TOPOLOGICALLY_PROTECTED".to_string()
    } else {
        "MZM_BULK_POLLUTION".to_string()
    };

    Ok(MajoranaZeroModeReceipt {
        chain_length_l: l,
        total_modes_audited: total_modes,
        unpaired_zero_modes: edge_modes,
        bulk_bonded_modes,
        is_boundary_isolated,
        mzm_status,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use num_bigint::BigInt;

    #[test]
    fn gin_index_lookup_and_involution_partner_test() {
        let mut gin = GinIndex::new();
        // 4 sites, 2 particles
        let mut occ1 = BTreeSet::new();
        occ1.insert(1);
        occ1.insert(2);
        gin.index_configuration(1, "Bipartite", occ1, 4, BigRational::from(BigInt::from(5)), 1, 1);

        let mut occ2 = BTreeSet::new();
        occ2.insert(2);
        occ2.insert(3);
        gin.index_configuration(2, "Bipartite", occ2, 4, BigRational::from(BigInt::from(5)), -1, 1);

        // Query mode 2
        let mut req = BTreeSet::new();
        req.insert(2);
        let res = gin.query_by_modes(&req, &BTreeSet::new());
        assert_eq!(res.len(), 2);
        assert!(res.contains(&1) && res.contains(&2));

        // Audit involution pair (1, 2)
        let receipt = gin.audit_involution_cancellations("Bipartite", &[(1, 2)]);
        assert!(receipt.all_exact_cancellations);
        assert_eq!(receipt.terminal_route, "ExactRepair");
    }

    #[test]
    fn kitaev_chain_majorana_zero_mode_isolation_test() {
        let receipt = audit_kitaev_chain_majorana(4).unwrap();
        assert_eq!(receipt.total_modes_audited, 8);
        assert_eq!(receipt.unpaired_zero_modes, vec![1, 8]);
        assert_eq!(receipt.bulk_bonded_modes, vec![2, 3, 4, 5, 6, 7]);
        assert!(receipt.is_boundary_isolated);
        assert_eq!(receipt.mzm_status, "MZM_TOPOLOGICALLY_PROTECTED");
    }
}
