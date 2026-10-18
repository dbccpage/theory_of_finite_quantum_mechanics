//! Dimension-four Clifton-Kent campaign table. AuthorityEffect: None.
use crate::linear_algebra::matrix as mx;
use omega_number_theory::cyclotomic::Cyc24;
use omega_number_theory::rational::{r_zero, rq};
use omega_quantum_physics::mub::algebra::ProjectorAlgebraStatus;
use omega_quantum_physics::mub::MubSystem;
use serde::{Deserialize, Serialize};
#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct CliftonKentDeficitReceipt {
    pub total_valuations: usize,
    pub non_psd_valuations: usize,
    pub non_psd_percentage: f64,
    pub purity_all_four: bool,
    pub trace_all_one: bool,
    pub sylvester_negative_minors_verified: bool,
    pub contextuality_persists_unconditionally: bool,
}

/// Evaluates the Clifton-Kent non-PSD deficit across all 4^5 = 1,024 classical valuations on d=4 MUBs.
pub fn evaluate_all_1024_clifton_kent_valuations(
    system: &MubSystem<Cyc24>,
) -> Result<CliftonKentDeficitReceipt, String> {
    if system.dimension != 4
        || system.verify_projector_algebra().status != ProjectorAlgebraStatus::AlgebraVerified
        || !system.is_complete()
    {
        return Err("expected a checked complete dimension-four MUB carrier".into());
    }
    let eye4 = mx::identity::<Cyc24>(4).map_err(|e| e.to_string())?;
    let one = Cyc24::one();
    let four = Cyc24::rat(rq(4, 1));
    let r_zero_val = r_zero();

    let mut non_psd_count = 0usize;
    let mut purity_all_four = true;
    let mut trace_all_one = true;
    let mut sylvester_all_negative = true;

    for v0 in 0..4 {
        for v1 in 0..4 {
            for v2 in 0..4 {
                for v3 in 0..4 {
                    for v4 in 0..4 {
                        let mut sum = mx::zeros::<Cyc24>(4, 4).map_err(|e| e.to_string())?;
                        sum = mx::add(
                            &sum,
                            system.try_projector(0, v0).map_err(|e| e.to_string())?,
                        )
                        .map_err(|e| e.to_string())?;
                        sum = mx::add(
                            &sum,
                            system.try_projector(1, v1).map_err(|e| e.to_string())?,
                        )
                        .map_err(|e| e.to_string())?;
                        sum = mx::add(
                            &sum,
                            system.try_projector(2, v2).map_err(|e| e.to_string())?,
                        )
                        .map_err(|e| e.to_string())?;
                        sum = mx::add(
                            &sum,
                            system.try_projector(3, v3).map_err(|e| e.to_string())?,
                        )
                        .map_err(|e| e.to_string())?;
                        sum = mx::add(
                            &sum,
                            system.try_projector(4, v4).map_err(|e| e.to_string())?,
                        )
                        .map_err(|e| e.to_string())?;
                        let rho = mx::sub(&sum, &eye4).map_err(|e| e.to_string())?;

                        if mx::trace(&rho).map_err(|e| e.to_string())? != one {
                            trace_all_one = false;
                        }

                        let rho_sq = mx::multiply(&rho, &rho).map_err(|e| e.to_string())?;
                        if mx::trace(&rho_sq).map_err(|e| e.to_string())? != four {
                            purity_all_four = false;
                        }

                        let mut has_negative_minor = false;
                        for i in 0..4 {
                            for j in (i + 1)..4 {
                                let diag_prod = rho
                                    .get_ref(i, i)
                                    .map_err(|e| e.to_string())?
                                    .mul(rho.get_ref(j, j).map_err(|e| e.to_string())?);
                                let off_diag = rho.get_ref(i, j).map_err(|e| e.to_string())?;
                                let off_diag_norm = off_diag.mul(&off_diag.conj());
                                let minor = diag_prod.sub(&off_diag_norm);
                                if let Some(r) = minor.as_rational() {
                                    if r < r_zero_val {
                                        has_negative_minor = true;
                                        break;
                                    }
                                }
                            }
                            if has_negative_minor {
                                break;
                            }
                        }

                        if has_negative_minor {
                            non_psd_count += 1;
                        } else {
                            sylvester_all_negative = false;
                        }
                    }
                }
            }
        }
    }

    let total = 1024usize;
    let pct = (non_psd_count as f64 / total as f64) * 100.0;
    let persists = non_psd_count == total && purity_all_four && trace_all_one;

    Ok(CliftonKentDeficitReceipt {
        total_valuations: total,
        non_psd_valuations: non_psd_count,
        non_psd_percentage: pct,
        purity_all_four,
        trace_all_one,
        sylvester_negative_minors_verified: sylvester_all_negative,
        contextuality_persists_unconditionally: persists,
    })
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_all_1024_clifton_kent_valuations_certified() {
        let mub4 = MubSystem::mub_d4();
        let receipt = evaluate_all_1024_clifton_kent_valuations(&mub4).unwrap();
        assert_eq!(receipt.total_valuations, 1024);
        assert_eq!(receipt.non_psd_valuations, 1024);
        assert!(receipt.purity_all_four);
        assert!(receipt.trace_all_one);
        assert!(receipt.sylvester_negative_minors_verified);
        assert!(receipt.contextuality_persists_unconditionally);
    }
}
