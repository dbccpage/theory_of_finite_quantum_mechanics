//! Local-Green / Global-Red (LGGR) **diagnostic** witness on GF(2) schedules.
//!
//! LGGR shape (CODE_DEMO):
//! - **Local green:** \(d_1 \omega = 0 \pmod 2\) (syndrome / face residual vanishes).
//! - **Global red:** schedule class is `ClosedResidual` (closed but not Exact).
//!
//! This is evaluator incompleteness of the coboundary layer, **not** GlobalGreen
//! authority and **not** FOC StabilizedSurvivor.
//!
//! AuthorityEffect: None on every witness receipt field.

use crate::gf2_terminalizer::{
    GF2Matrix, GF2ScheduleStatus, Gf2CocycleClassifier, Gf2ScheduleReceipt,
};

/// LGGR diagnostic witness. Never mints authority.
#[derive(Debug, Clone)]
pub struct LggrWitness {
    /// \(d_1 \omega = 0 \pmod 2\).
    pub local_green: bool,
    /// Status is exactly `ClosedResidual` (not Exact, not Open).
    pub global_red: bool,
    /// Full LGGR: local green AND global red.
    pub is_lggr: bool,
    /// Face / higher residual of \(\omega\) (the local syndrome vector).
    pub d1_omega: Vec<u8>,
    /// Underlying schedule receipt (authority_effect always `"None"`).
    pub certificate: Gf2ScheduleReceipt,
}

/// Compute \(d_1 \omega \pmod 2\).
pub fn apply_d1(d1: &GF2Matrix, omega: &[u8]) -> Result<Vec<u8>, String> {
    if omega.len() != d1.cols {
        return Err(format!(
            "lggr: omega length {} != d1.cols {}",
            omega.len(),
            d1.cols
        ));
    }
    let mut out = vec![0u8; d1.rows];
    for i in 0..d1.rows {
        let mut sum = 0u8;
        for j in 0..d1.cols {
            sum ^= d1.data[i][j] & (omega[j] % 2);
        }
        out[i] = sum & 1;
    }
    Ok(out)
}

/// Detect LGGR on a declared complex and residual 1-cochain.
///
/// Requires a valid boundary (\(d_1 d_0 = 0\)); refuses otherwise via `terminalize`.
pub fn detect_lggr(d0: &GF2Matrix, d1: &GF2Matrix, omega: &[u8]) -> Result<LggrWitness, String> {
    let certificate = Gf2CocycleClassifier::classify(d0, d1, omega)?;
    let d1_omega = apply_d1(d1, omega)?;
    let local_green = d1_omega.iter().all(|&v| v == 0);
    let global_red = certificate.status == GF2ScheduleStatus::ClosedResidual;
    Ok(LggrWitness {
        local_green,
        global_red,
        is_lggr: local_green && global_red,
        d1_omega,
        certificate,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::complexes::{
        exact_syndrome_example, open_syndrome_example, surface_grid_2x2_torus, triangle,
        torus_logical_x_example,
    };
    use crate::gf2_terminalizer::{GF2Matrix, GF2ScheduleStatus};

    #[test]
    fn torus_logical_is_lggr() {
        let c = surface_grid_2x2_torus();
        let w = detect_lggr(&c.d0, &c.d1, &torus_logical_x_example()).unwrap();
        assert!(w.local_green, "d1 omega must be all-zero");
        assert!(w.global_red, "must be ClosedResidual");
        assert!(w.is_lggr);
        assert_eq!(w.d1_omega, vec![0, 0, 0, 0]);
        assert_eq!(w.certificate.status, GF2ScheduleStatus::ClosedResidual);
        assert_eq!(w.certificate.authority_effect, "None");
    }

    #[test]
    fn exact_syndrome_is_not_lggr() {
        // Kills: setting is_lggr from local_green alone, so every coboundary counts as LGGR.
        let c = triangle();
        let w = detect_lggr(&c.d0, &c.d1, &exact_syndrome_example()).unwrap();
        assert!(w.local_green);
        assert_eq!(w.d1_omega, vec![0]);
        assert!(!w.global_red);
        assert!(!w.is_lggr);
        assert_eq!(w.certificate.status, GF2ScheduleStatus::Exact);
    }

    #[test]
    fn open_obstruction_is_not_lggr() {
        // Kills: treating every non-Exact class as LGGR, or ignoring a nonzero face syndrome.
        let c = triangle();
        let w = detect_lggr(&c.d0, &c.d1, &open_syndrome_example()).unwrap();
        assert_eq!(w.d1_omega, vec![1]);
        assert!(!w.local_green);
        assert!(!w.global_red);
        assert!(!w.is_lggr);
        assert_eq!(w.certificate.status, GF2ScheduleStatus::OpenObstruction);
    }

    #[test]
    fn length_mismatch_returns_err() {
        // Kills: skipping the length check and returning Ok on a short residual.
        let c = triangle();
        let err = detect_lggr(&c.d0, &c.d1, &[1, 0]).unwrap_err();
        assert!(
            err.contains("Syndrome dimension"),
            "short residual must be refused, got {err}"
        );
        let err = apply_d1(&c.d1, &[1]).unwrap_err();
        assert!(
            err.contains("omega length"),
            "apply_d1 must refuse a short vector, got {err}"
        );
    }

    #[test]
    fn non_complex_is_refused() {
        // Kills: classifying a pair with d1*d0 != 0 instead of refusing it.
        let c = triangle();
        let bad_d1 = GF2Matrix::from_data(vec![vec![1, 0, 0]]);
        let mut prod = vec![0u8; c.d0.cols];
        for (k, row) in c.d0.data.iter().enumerate() {
            if bad_d1.data[0][k] == 1 {
                for (j, bit) in row.iter().enumerate() {
                    prod[j] ^= bit & 1;
                }
            }
        }
        assert_ne!(prod, vec![0, 0, 0], "fixture must actually break d1*d0");
        let err = detect_lggr(&c.d0, &bad_d1, &[1, 0, 0]).unwrap_err();
        assert!(
            err.contains("d1 * d0"),
            "non-complex must be refused, got {err}"
        );
    }
}
