//! End-to-end residual classifier: residual -> terminal + receipt.
//!
//! [`Gf2CocycleClassifier`] already decides the three-way split correctly. This
//! module *refines* it -- it does not re-derive it -- by adding the cohomology
//! data a `ClosedResidual` needs before it can be called a named logical error:
//!
//! ```text
//! d1 . d0 != 0, or bad shape          -> RepresentationInvalid
//! r in im d0                          -> Exact
//! d1 r != 0                           -> OpenObstruction
//! closed, non-exact, Phi_1 capped     -> ClosedResidual   (honest fallback)
//! closed, non-exact, Phi_1 certified  -> TypedHarmonic    (class + witness)
//! ```
//!
//! `TypedHarmonic` strictly dominates `ClosedResidual`; it is not a rename.
//! When the l1 search hits its budget the terminal degrades, so the pipeline
//! never asserts a minimum it did not compute.
//!
//! Python dual face: `omega_engine/omega_engine_majorana/engines/classifier.py`.
//!
//! Every receipt carries `authority_effect = "None"`.

use serde::{Deserialize, Serialize};

use crate::gf2_terminalizer::{GF2Matrix, Gf2CocycleClassifier};
use crate::harmonic::{h1_basis, l1_harmonic_projection, H1Basis, DEFAULT_BUDGET};
use crate::repair_limit::{apply_d0, apply_d1, gf2_add, in_image_d0, solve_d0};

/// Receipt tag for classified residuals.
pub const CLASSIFIED_RECEIPT_TAG: &str = "omega.majorana-tetron-classified.v1";

/// Every terminal the classifier can emit.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum Terminal {
    Exact,
    OpenObstruction,
    ClosedResidual,
    TypedHarmonic,
    RepresentationInvalid,
}

impl Terminal {
    /// Physical reading, carried into the receipt.
    pub fn reading(self) -> &'static str {
        match self {
            Terminal::Exact => "pure gauge: an MZM reference-frame relabelling; no defect",
            Terminal::OpenObstruction => {
                "an island parity constraint is violated; a localized \
                 violated declared island parity relation, named by the coherence \n                 witness; physical cause UNDETERMINED"
            }
            Terminal::ClosedResidual => {
                "consistent with every island constraint but not gauge: a logical \
                 parity error whose minimum weight was not certified"
            }
            Terminal::TypedHarmonic => {
                "a logical parity error, identified in the H^1 basis, with a \
                 certified minimum-weight witness"
            }
            Terminal::RepresentationInvalid => "the declared carrier is not a cochain complex",
        }
    }
}

/// Classification receipt. `AuthorityEffect: None` always.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ClassifiedReceipt {
    pub certificate_tag: String,
    pub terminal: Terminal,
    pub terminal_reading: String,
    pub reason: String,
    pub dim_h1: Option<usize>,
    pub class_coordinates: Option<Vec<u8>>,
    pub class_id: Option<String>,
    pub coherence_witness: Option<Vec<u8>>,
    /// For `Exact` only: a genuine solution of `d0 * alpha = r`, constructed by
    /// [`solve_d0`]. NEVER the capped Phi1 search's alpha — that vector minimizes
    /// weight within the budget and is `0` when the budget stops early, which
    /// would publish a false witness for a residual that really is exact.
    pub certificate_alpha: Option<Vec<u8>>,
    /// Self-check on the field above: `d0 * certificate_alpha == r`. `None` when
    /// no witness is published. This checks the equation actually CLAIMED, unlike
    /// `phi1_verified`, which checks `r + d0 * phi1_alpha == representative`.
    pub certificate_verified: Option<bool>,
    pub phi1_weight: Option<usize>,
    pub phi1_exact: Option<bool>,
    pub phi1_representative: Option<Vec<u8>>,
    pub phi1_alpha: Option<Vec<u8>>,
    pub phi1_searched: Option<u64>,
    pub phi1_coset_size: Option<u64>,
    /// Self-check: the reported witness really does produce the representative.
    pub phi1_verified: Option<bool>,
    pub authority_effect: String,
}

fn invalid(reason: &str) -> ClassifiedReceipt {
    ClassifiedReceipt {
        certificate_tag: CLASSIFIED_RECEIPT_TAG.to_string(),
        terminal: Terminal::RepresentationInvalid,
        terminal_reading: Terminal::RepresentationInvalid.reading().to_string(),
        reason: reason.to_string(),
        dim_h1: None,
        class_coordinates: None,
        class_id: None,
        coherence_witness: None,
        certificate_alpha: None,
        certificate_verified: None,
        phi1_weight: None,
        phi1_exact: None,
        phi1_representative: None,
        phi1_alpha: None,
        phi1_searched: None,
        phi1_coset_size: None,
        phi1_verified: None,
        authority_effect: "None".to_string(),
    }
}

/// Classify `residual` against the complex `(d0, d1)`.
///
/// `budget` caps the l1 coset search; exceeding it degrades `TypedHarmonic` to
/// `ClosedResidual` rather than guessing.
pub fn classify(d0: &GF2Matrix, d1: &GF2Matrix, residual: &[u8], budget: u64) -> ClassifiedReceipt {
    classify_inner(d0, d1, residual, budget, false)
}

/// Classify, and additionally run the l1 coset search even on the polynomial
/// terminals so gauge-minimal diagnostics are available.
///
/// This is the pre-review behaviour, kept as an EXPLICIT request. [`classify`]
/// short-circuits because both `Exact` and `OpenObstruction` are decided by
/// polynomial linear algebra; paying the exponential search for them made the
/// advertised end-to-end cost unattainable.
pub fn classify_with_diagnostics(
    d0: &GF2Matrix,
    d1: &GF2Matrix,
    residual: &[u8],
    budget: u64,
) -> ClassifiedReceipt {
    classify_inner(d0, d1, residual, budget, true)
}

fn classify_inner(
    d0: &GF2Matrix,
    d1: &GF2Matrix,
    residual: &[u8],
    budget: u64,
    always_project: bool,
) -> ClassifiedReceipt {
    if residual.len() != d0.rows {
        return invalid("residual length does not match the channel count");
    }
    if !Gf2CocycleClassifier::verify_boundary(d0, d1) {
        return invalid("d1 * d0 != 0");
    }

    let normalized: Vec<u8> = residual.iter().map(|value| value % 2).collect();
    let basis = h1_basis(d0, d1);
    let coordinates = basis.class_coordinates(&normalized);

    // REVIEW P2 -- API boundary. Both terminals below are decided by POLYNOMIAL
    // linear algebra. Running the exponential l1 coset search before them made
    // every classification pay for it, so the advertised end-to-end cost was not
    // the cost anyone actually observed. The search now runs only on the branch
    // that needs it.
    let syndrome = match apply_d1(d1, &normalized) {
        Ok(syndrome) => syndrome,
        Err(reason) => return invalid(&reason),
    };
    let is_open = syndrome.contains(&1);
    let is_exact = in_image_d0(d0, &normalized).unwrap_or(false);

    // Phi1 is skipped on the polynomial terminals. For `Exact` its value is known
    // ANALYTICALLY rather than guessed: r in im(d0) means some alpha gives
    // r + d0*alpha = 0, so the l1 minimum is 0 and it is attained. For
    // `OpenObstruction` a gauge-minimal representative is not part of the verdict.
    let projection = if (is_open || is_exact) && !always_project {
        None
    } else {
        match l1_harmonic_projection(d0, &normalized, budget) {
            Ok(projection) => Some(projection),
            Err(reason) => return invalid(&reason),
        }
    };
    let verified = projection.as_ref().map(|p| {
        apply_d0(d0, &p.alpha)
            .and_then(|image| gf2_add(&normalized, &image))
            .map(|combined| combined == p.representative)
            .unwrap_or(false)
    });

    let (terminal, reason, witness) = if is_exact {
        (Terminal::Exact, "residual lies in im(d0)".to_string(), None)
    } else if is_open {
        (
            Terminal::OpenObstruction,
            "d1 * r != 0".to_string(),
            Some(syndrome),
        )
    } else if let (Some(true), Some(coords)) =
        (projection.as_ref().map(|p| p.exact), coordinates.as_ref())
    {
        let label = H1Basis::class_id(coords);
        (
            Terminal::TypedHarmonic,
            format!(
                "nontrivial class {} in H^1 (dim {}); l1-minimal weight {} certified",
                label,
                basis.dim,
                projection.as_ref().map(|p| p.weight).unwrap_or(0)
            ),
            None,
        )
    } else {
        (
            Terminal::ClosedResidual,
            "r not in im(d0) and d1 * r = 0; l1 minimum not certified".to_string(),
            None,
        )
    };

    // The Exact witness is CONSTRUCTED, not borrowed from the capped search.
    let certificate_alpha = if terminal == Terminal::Exact {
        solve_d0(d0, &normalized).ok().flatten()
    } else {
        None
    };
    let certificate_verified = certificate_alpha.as_ref().map(|alpha| {
        apply_d0(d0, alpha)
            .map(|image| image == normalized)
            .unwrap_or(false)
    });

    ClassifiedReceipt {
        certificate_tag: CLASSIFIED_RECEIPT_TAG.to_string(),
        terminal,
        terminal_reading: terminal.reading().to_string(),
        reason,
        dim_h1: Some(basis.dim),
        class_id: coordinates.as_ref().map(|c| H1Basis::class_id(c)),
        class_coordinates: coordinates,
        coherence_witness: witness,
        certificate_alpha,
        certificate_verified,
        // Exact: the l1 minimum is 0 and attained (r + d0*certificate_alpha = 0),
        // known analytically, not searched. Open: not part of the verdict.
        phi1_weight: match (&projection, terminal) {
            (Some(p), _) => Some(p.weight),
            (None, Terminal::Exact) => Some(0),
            _ => None,
        },
        phi1_exact: match (&projection, terminal) {
            (Some(p), _) => Some(p.exact),
            (None, Terminal::Exact) => Some(true),
            _ => None,
        },
        phi1_representative: projection.as_ref().map(|p| p.representative.clone()),
        phi1_alpha: projection.as_ref().map(|p| p.alpha.clone()),
        phi1_searched: projection.as_ref().map(|p| p.searched),
        phi1_coset_size: projection.as_ref().map(|p| p.coset_size),
        phi1_verified: verified,
        authority_effect: "None".to_string(),
    }
}

/// Classify with the default budget.
pub fn classify_default(d0: &GF2Matrix, d1: &GF2Matrix, residual: &[u8]) -> ClassifiedReceipt {
    classify(d0, d1, residual, DEFAULT_BUDGET)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::tetron::{build_tetron_array, logical_class_representative, Axis, Topology};

    #[test]
    fn torus_reaches_every_terminal() {
        let (complex, report) = build_tetron_array(3, 3, Topology::Torus).unwrap();
        let mut alpha = vec![0u8; report.num_mzm];
        alpha[0] = 1;
        let gauge = apply_d0(&complex.d0, &alpha).unwrap();
        let mut single = vec![0u8; report.num_channels];
        single[0] = 1;
        let logical = logical_class_representative(&report, Axis::Column, 0);

        assert_eq!(
            classify_default(&complex.d0, &complex.d1, &gauge).terminal,
            Terminal::Exact
        );
        assert_eq!(
            classify_default(&complex.d0, &complex.d1, &single).terminal,
            Terminal::OpenObstruction
        );
        assert_eq!(
            classify_default(&complex.d0, &complex.d1, &logical).terminal,
            Terminal::TypedHarmonic
        );
        assert_eq!(
            classify(&complex.d0, &complex.d1, &logical, 4).terminal,
            Terminal::ClosedResidual
        );
    }

    #[test]
    fn disk_never_yields_a_logical_class() {
        let (complex, report) = build_tetron_array(3, 3, Topology::Disk).unwrap();
        let mut state: u64 = 3;
        for _ in 0..120 {
            let residual: Vec<u8> = (0..report.num_channels)
                .map(|_| {
                    state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
                    ((state >> 33) & 1) as u8
                })
                .collect();
            let terminal = classify_default(&complex.d0, &complex.d1, &residual).terminal;
            assert!(
                terminal == Terminal::Exact || terminal == Terminal::OpenObstruction,
                "H^1 = 0 cannot produce {terminal:?}"
            );
        }
    }

    #[test]
    fn typed_harmonic_receipt_is_complete() {
        let (complex, report) = build_tetron_array(3, 4, Topology::Torus).unwrap();
        let residual = logical_class_representative(&report, Axis::Column, 0);
        let receipt = classify_default(&complex.d0, &complex.d1, &residual);
        assert_eq!(receipt.terminal, Terminal::TypedHarmonic);
        assert_eq!(receipt.phi1_exact, Some(true));
        assert_eq!(receipt.phi1_verified, Some(true));
        assert_eq!(receipt.dim_h1, Some(2));
        assert!(receipt.class_coordinates.as_ref().unwrap().contains(&1));
        assert!(receipt.class_id.as_ref().unwrap().starts_with("h1:"));
        assert_eq!(receipt.authority_effect, "None");
    }

    #[test]
    fn capped_search_falls_back_and_never_claims_exactness() {
        let (complex, report) = build_tetron_array(3, 4, Topology::Torus).unwrap();
        let residual = logical_class_representative(&report, Axis::Column, 0);
        let capped = classify(&complex.d0, &complex.d1, &residual, 4);
        let full = classify_default(&complex.d0, &complex.d1, &residual);
        assert_eq!(capped.terminal, Terminal::ClosedResidual);
        assert_eq!(capped.phi1_exact, Some(false));
        // the class is still known -- only the minimum weight is not certified
        assert!(capped.class_coordinates.as_ref().unwrap().contains(&1));
        assert!(capped.phi1_weight >= full.phi1_weight);
    }

    #[test]
    fn open_obstruction_has_no_class_but_keeps_phi1() {
        let (complex, report) = build_tetron_array(3, 3, Topology::Torus).unwrap();
        let mut residual = vec![0u8; report.num_channels];
        residual[5] = 1;
        // Phi1 on an OpenObstruction is now an EXPLICIT request (review P2):
        // `classify` short-circuits, `classify_with_diagnostics` does not.
        let receipt =
            classify_with_diagnostics(&complex.d0, &complex.d1, &residual, DEFAULT_BUDGET);
        assert_eq!(receipt.terminal, Terminal::OpenObstruction);
        assert!(receipt.class_coordinates.is_none());
        assert!(receipt.class_id.is_none());
        assert_eq!(receipt.phi1_weight, Some(1));
        assert_eq!(
            receipt
                .coherence_witness
                .as_ref()
                .unwrap()
                .iter()
                .filter(|&&b| b == 1)
                .count(),
            2,
            "a channel borders exactly two islands"
        );
    }

    #[test]
    fn representation_invalid_is_refused_not_classified() {
        let d0 = GF2Matrix::from_data(vec![vec![1, 0], vec![0, 1]]);
        let d1 = GF2Matrix::from_data(vec![vec![1, 0]]);
        let receipt = classify_default(&d0, &d1, &[1, 0]);
        assert_eq!(receipt.terminal, Terminal::RepresentationInvalid);
        assert!(receipt.class_coordinates.is_none());
        assert_eq!(receipt.authority_effect, "None");

        let (complex, _) = build_tetron_array(2, 2, Topology::Torus).unwrap();
        let short = classify_default(&complex.d0, &complex.d1, &[1, 0]);
        assert_eq!(short.terminal, Terminal::RepresentationInvalid);
    }

    #[test]
    fn class_id_is_stable_across_representatives_of_one_class() {
        let (complex, report) = build_tetron_array(3, 3, Topology::Torus).unwrap();
        let logical = logical_class_representative(&report, Axis::Row, 0);
        let baseline = classify_default(&complex.d0, &complex.d1, &logical);
        let mut state: u64 = 2718;
        for _ in 0..6 {
            let alpha: Vec<u8> = (0..report.num_mzm)
                .map(|_| {
                    state = state.wrapping_mul(6364136223846793005).wrapping_add(1);
                    ((state >> 33) & 1) as u8
                })
                .collect();
            let shifted = gf2_add(&logical, &apply_d0(&complex.d0, &alpha).unwrap()).unwrap();
            let moved = classify_default(&complex.d0, &complex.d1, &shifted);
            assert_eq!(moved.class_id, baseline.class_id);
            assert_eq!(moved.phi1_weight, baseline.phi1_weight);
        }
    }

    #[test]
    fn receipt_serializes_the_typed_harmonic_class() {
        // Kills: writing authority None while the terminal stays ClosedResidual or Exact.
        let (complex, report) = build_tetron_array(2, 2, Topology::Torus).unwrap();
        let residual = logical_class_representative(&report, Axis::Column, 0);
        let receipt = classify_default(&complex.d0, &complex.d1, &residual);
        assert_eq!(receipt.terminal, Terminal::TypedHarmonic);
        assert_eq!(receipt.dim_h1, Some(2));
        assert_eq!(receipt.phi1_exact, Some(true));
        assert!(receipt.class_coordinates.as_ref().unwrap().contains(&1));
        assert!(receipt.certificate_alpha.is_none());
        let json = serde_json::to_string(&receipt).unwrap();
        assert!(json.contains("\"terminal\":\"TypedHarmonic\""));
        assert!(json.contains("\"authority_effect\":\"None\""));
        assert!(json.contains(CLASSIFIED_RECEIPT_TAG));
        assert!(!json.contains("PROVED"));
        assert!(!json.contains("CertifiedAuthority"));
    }
}

#[cfg(test)]
mod review_p1_reproduction {
    use super::*;

    /// REVIEW P1 REPRODUCTION (pre-fix this FAILS, which is the point).
    ///
    /// With a budget that stops the coset search before it reaches the true
    /// solution, `projection.alpha` can be `0` while `in_image_d0` independently
    /// (and correctly) decides `Exact`. The receipt then publishes
    /// `certificate_alpha = 0` for a residual with `d0 * 0 != r`.
    #[test]
    fn p1_capped_exact_must_not_publish_a_false_witness() {
        // d0 with a nonzero image: 3 channels, 2 generators.
        let d0 = GF2Matrix::from_data(vec![vec![1, 0], vec![1, 1], vec![0, 1]]);
        // d1 = 0 (single zero row) so d1*d0 = 0 and nothing is OpenObstruction.
        let d1 = GF2Matrix::from_data(vec![vec![0, 0, 0]]);

        // r = d0 * alpha for alpha = (1,0)  ->  r = (1,1,0), certainly exact.
        let alpha_true = vec![1u8, 0u8];
        let r = apply_d0(&d0, &alpha_true).expect("apply");
        assert_eq!(r, vec![1, 1, 0]);
        assert!(in_image_d0(&d0, &r).unwrap(), "r is in im(d0)");

        // Budget 1: the search examines only the representative itself.
        let receipt = classify(&d0, &d1, &r, 1);
        assert_eq!(receipt.terminal, Terminal::Exact, "membership says Exact");

        // The published witness must actually satisfy d0 * alpha = r.
        let alpha = receipt
            .certificate_alpha
            .clone()
            .expect("Exact receipts carry a witness");
        let image = apply_d0(&d0, &alpha).expect("apply");
        assert_eq!(
            image, r,
            "PUBLISHED WITNESS IS INVALID: d0 * certificate_alpha != r \
             (alpha={alpha:?}, d0*alpha={image:?}, r={r:?})"
        );
    }
}

#[cfg(test)]
mod review_p1_invariants {
    use super::*;
    use crate::tetron::{build_tetron_array, Topology};

    /// Whenever a witness is published it must verify. Swept over a family so
    /// the single reproduction fixture cannot be the only case that holds.
    #[test]
    fn p1_published_witness_always_verifies() {
        let d0 = GF2Matrix::from_data(vec![vec![1, 0], vec![1, 1], vec![0, 1]]);
        let d1 = GF2Matrix::from_data(vec![vec![0, 0, 0]]);
        let mut exact_seen = 0;
        for a in 0..4u8 {
            let alpha = vec![a & 1, (a >> 1) & 1];
            let r = apply_d0(&d0, &alpha).expect("apply");
            // every budget from "stops immediately" to "exhausts the coset"
            for budget in [1u64, 2, 3, 4, 64] {
                let receipt = classify(&d0, &d1, &r, budget);
                if receipt.terminal == Terminal::Exact {
                    exact_seen += 1;
                    assert_eq!(
                        receipt.certificate_verified,
                        Some(true),
                        "Exact receipt must carry a verified witness (budget {budget})"
                    );
                    let alpha_pub = receipt.certificate_alpha.expect("witness present");
                    assert_eq!(apply_d0(&d0, &alpha_pub).unwrap(), r);
                }
            }
        }
        assert!(
            exact_seen >= 5,
            "sweep must actually reach Exact, saw {exact_seen}"
        );
    }

    /// `certificate_alpha` is published for `Exact` only.
    #[test]
    fn p1_witness_only_on_exact() {
        // b1 = 1 cycle: d0 maps 2 vertices -> 2 edges, r = (1,0) is not exact.
        let d0 = GF2Matrix::from_data(vec![vec![1, 1], vec![1, 1]]);
        let d1 = GF2Matrix::from_data(vec![vec![0, 0]]);
        let receipt = classify(&d0, &d1, &[1, 0], 64);
        assert_ne!(receipt.terminal, Terminal::Exact);
        assert!(receipt.certificate_alpha.is_none());
        assert!(receipt.certificate_verified.is_none());
    }

    /// The solver refuses inconsistent systems rather than inventing a witness.
    #[test]
    fn p1_solver_returns_none_off_image() {
        let d0 = GF2Matrix::from_data(vec![vec![1, 0], vec![1, 1], vec![0, 1]]);
        // (1,0,0) is not in im(d0): the three rows force a2 = 0, a1 = 1 and a1 = 1...
        let off = vec![1u8, 0, 0];
        assert!(
            !in_image_d0(&d0, &off).unwrap(),
            "fixture must be off-image"
        );
        assert_eq!(solve_d0(&d0, &off).unwrap(), None);
    }

    /// A 6×6 torus has 72 channels. Weight one is open, and the short-circuit
    /// classify does not run the exponential coset search.
    #[test]
    fn six_by_six_torus_weight_one_is_open_within_a_tenth_of_a_second() {
        let (complex, report) = build_tetron_array(6, 6, Topology::Torus).unwrap();
        assert_eq!(report.num_channels, 72);
        assert_eq!(report.num_mzm, 36);
        assert_eq!(report.dim_h1, 2);
        assert_eq!(report.expected_dim_h1, 2);
        assert!(report.homology_matches_prediction());
        let mut residual = vec![0u8; report.num_channels];
        residual[0] = 1;
        let started = std::time::Instant::now();
        let receipt = classify(&complex.d0, &complex.d1, &residual, 64);
        let elapsed = started.elapsed();
        assert_eq!(receipt.terminal, Terminal::OpenObstruction);
        assert_eq!(receipt.dim_h1, Some(2));
        assert_eq!(receipt.authority_effect, "None");
        assert!(receipt.certificate_alpha.is_none());
        assert!(receipt.phi1_searched.is_none());
        assert!(receipt
            .coherence_witness
            .as_ref()
            .is_some_and(|witness| witness.contains(&1)));
        assert!(
            elapsed.as_millis() < 100,
            "in-process classify took {elapsed:?}"
        );
    }
}
