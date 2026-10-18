//! LGGR II organizational gluing + LGGR III EPK→CODA_GTLA overlay.
//!
//! # What this module refuses to encode
//!
//! LGGR II §4 states a boxed condition:
//!
//! ```text
//! G_rep(b) ∧ G_auth(b) ∧ G_time(b)  ⟹  E_G(b) = ∏ᵢ Eᵢ(b)
//! ```
//!
//! and immediately types it **`[DEFINITION]`**, not a theorem: *"This box is not a
//! fresh theorem. … the three conditions are *defined* to name the ways that
//! factorization can fail at an organizational boundary, not derived premises that
//! force it."*
//!
//! Lemma 4.4 then closes the question in the negative, mechanized:
//!
//! > *"If `G_rep` is read only as representational sufficiency … then
//! > `G_rep ∧ G_auth ∧ G_time` does **not** imply `E_G = ∏ᵢ Eᵢ`. The finite Boolean
//! > witness is one boundary with `E₁ = E₂ = 1`, `E_G = 0`, representation
//! > `R = (1,1,0)`, and both `G_auth` and `G_time` true."*
//!
//! (Lean: `PaperAE005.weak_boundary_sufficiency_does_not_force_factorization`,
//! reported axiom-free.) The paper also records that strengthening `G_rep` into
//! product-sufficiency makes it *equivalent to evaluator factorization itself*, so
//! it is not an independent premise.
//!
//! Therefore this module provides **no** function asserting that the gate
//! conjunction implies factorization. [`gate_sufficiency_status`] exists precisely
//! to return why that claim is unavailable under either reading.
//!
//! **The contrapositive is refuted too.** A proposition and its contrapositive are
//! logically equivalent, so once Lemma 4.4 refutes the implication it equally
//! refutes `Δ_E ≠ 0 ⟹ ¬G_rep ∨ ¬G_auth ∨ ¬G_time`. The Lemma 4.4 witness is a
//! counterexample to both: all three gates hold and `Δ_E = -1`. An earlier
//! revision of this comment claimed the contrapositive was still load-bearing;
//! that was wrong.
//!
//! What survives: a nonzero `Δ_E` exhibits evaluator non-factorization **in the
//! declared model**. Under the weak gate definitions it neither identifies nor
//! entails failure of any particular upstream gate.
//!
//! The published reference stub `020/code/lggr_ii_organizational_gluing.py`
//! implements `is_closure_eligible` as `owner.has_authority and
//! owner.has_accountability` — `G_auth` alone — under a name that reads as
//! sufficiency. [`closure_eligibility`] keeps the check but returns a type that
//! cannot be mistaken for a certificate.
//!
//! **AuthorityEffect: None.**

use serde::{Deserialize, Serialize};

use omega_types::authority::AuthorityEffect;

use crate::verdict::LggrVerdict;

// ── LGGR II: organizational closure conditions ───────────────────────────────

/// The named organizational closure conditions of LGGR II §4.1.
///
/// `GEval` is included because §5 and §8 list it in the conjunction. Note that the
/// published manuscript writes that conjunction as
/// `G_rep ∧ G_auth ∧ G_time ∧ G_eval ∧ G_eval` — **`G_eval` appears twice**
/// (020 lines 209 and 323). That is a defect in the published text, recorded here
/// and in the residual ledger; it is not reproduced as a duplicated field.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub enum OrganizationalGate {
    /// Representational sufficiency: the boundary representation carries enough
    /// information to determine `E_G` at the point of resolution.
    GRep,
    /// Authority closure: a declared boundary owner holds both authority over the
    /// local validators and accountability to the global evaluator.
    GAuth,
    /// Temporal coherence: local validation and global evaluation are gauged on a
    /// unified declared ordering.
    GTime,
    /// Evaluator condition, as listed in §5/§8.
    GEval,
}

/// How `G_rep` is being read. The distinction is load-bearing, not stylistic.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum GRepReading {
    /// "The boundary representation recovers `E_G`." Lemma 4.4 refutes sufficiency
    /// under this reading.
    Weak,
    /// "The boundary representation recovers `∏ᵢ Eᵢ` and `E_G` jointly." The paper
    /// records this as *equivalent to evaluator factorization itself*, so it is not
    /// an independent premise.
    ProductSufficiency,
}

/// Why the gate conjunction cannot be used as a sufficiency claim.
///
/// There is deliberately no variant meaning "the gates imply factorization".
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum GateSufficiencyStatus {
    /// Weak reading: refuted by the Lemma 4.4 Boolean counterexample.
    RefutedByLemma44,
    /// Product-sufficiency reading: holds, but only because the premise already
    /// *is* the conclusion. Circular, therefore not usable as an inference.
    CircularWithFactorization,
}

/// The status of the §4 box under a declared reading of `G_rep`.
///
/// This function is the whole point of the module's caution: it never returns
/// "sufficient".
pub fn gate_sufficiency_status(reading: GRepReading) -> GateSufficiencyStatus {
    match reading {
        GRepReading::Weak => GateSufficiencyStatus::RefutedByLemma44,
        GRepReading::ProductSufficiency => GateSufficiencyStatus::CircularWithFactorization,
    }
}

/// The finite Boolean witness of LGGR II Lemma 4.4.
///
/// `E₁ = E₂ = 1`, `E_G = 0`, representation `R = (1,1,0)`, `G_auth` and `G_time`
/// true, and weak `G_rep` satisfied because `E_G` is recoverable by projection
/// from `R`. Nevertheless `0 = E_G ≠ E₁·E₂ = 1`.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub struct Lemma44Witness {
    pub local_left_pass: bool,
    pub local_right_pass: bool,
    pub global_pass: bool,
    pub representation: [bool; 3],
    pub g_auth: bool,
    pub g_time: bool,
}

impl Default for Lemma44Witness {
    fn default() -> Self {
        Self {
            local_left_pass: true,
            local_right_pass: true,
            global_pass: false,
            representation: [true, true, false],
            g_auth: true,
            g_time: true,
        }
    }
}

impl Lemma44Witness {
    /// Weak `G_rep` holds: `E_G` is recoverable from the representation by
    /// projection onto its third component.
    pub fn weak_g_rep_holds(&self) -> bool {
        self.representation[2] == self.global_pass
    }

    /// Evaluator factorization `E_G = E₁ · E₂`.
    pub fn factorization_holds(&self) -> bool {
        self.global_pass == (self.local_left_pass && self.local_right_pass)
    }
}

/// A declared boundary owner: authority over the local validators, accountability
/// to the global evaluator.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct BoundaryOwner {
    pub name: String,
    pub has_authority: bool,
    pub has_accountability: bool,
}

/// The result of the closure-eligibility check.
///
/// LGGR II Lemma (Organizational Boundary Closure Eligibility) is explicit that
/// this is **necessary and not sufficient**: *"This is necessary for the declared
/// packet shape and not sufficient for empirical success or authority."*
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ClosureEligibility {
    /// `G_auth` present. A required field of the declared packet shape is
    /// satisfied — nothing more. This is **not** a certificate of closure.
    RequiredFieldPresent,
    /// No declared boundary owner object at all.
    NoDeclaredOwner,
    /// An owner exists but lacks authority to install boundary tests.
    OwnerLacksAuthority,
    /// An owner exists but is not accountable to the global evaluator.
    OwnerLacksAccountability,
    /// An owner exists with neither.
    OwnerLacksAuthorityAndAccountability,
}

impl ClosureEligibility {
    /// Whether the `G_auth` field is present. **Never** a closure certificate —
    /// the name says field, not closure, deliberately.
    pub fn required_field_present(&self) -> bool {
        matches!(self, Self::RequiredFieldPresent)
    }

    /// Whether this certifies closure. **Always false**, for every variant.
    pub fn certifies_closure(&self) -> bool {
        false
    }
}

/// Check `G_auth` for a boundary.
pub fn closure_eligibility(owner: Option<&BoundaryOwner>) -> ClosureEligibility {
    match owner {
        None => ClosureEligibility::NoDeclaredOwner,
        Some(o) => match (o.has_authority, o.has_accountability) {
            (true, true) => ClosureEligibility::RequiredFieldPresent,
            (false, true) => ClosureEligibility::OwnerLacksAuthority,
            (true, false) => ClosureEligibility::OwnerLacksAccountability,
            (false, false) => ClosureEligibility::OwnerLacksAuthorityAndAccountability,
        },
    }
}

/// The reading of a defect against the declared gates.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum GateChecklistReading {
    /// `Δ_E ≠ 0`: evaluator non-factorization is exhibited in the declared model.
    ///
    /// `candidates` restates the gates the **caller declared** as not holding. It
    /// is a convenience for an auditor reading their own declaration back — it is
    /// **not** inferred from the defect, and the defect entails nothing about any
    /// particular gate (Lemma 4.4).
    ///
    /// If `candidates` is empty the declaration itself is suspect: every gate was
    /// declared to hold and the defect is nonzero anyway, which is exactly the
    /// Lemma 4.4 situation under a weak `G_rep`.
    SomeConditionFailed {
        candidates: Vec<OrganizationalGate>,
        /// True when every gate was declared true despite a nonzero defect.
        contradicts_declaration: bool,
    },
    /// `Δ_E = 0` observed. LGGR II §5: an observed pass is not a certified closure,
    /// and §3.1 generalizes that from luck to detector capability.
    ObservedZeroNotCertified,
    /// The verdict carries no usable defect reading (oracle-extracted, §7.3).
    NoSoundReading,
}

/// Report a verdict alongside the caller's own gate declarations.
///
/// This performs **no inference**: `candidates` is a filter over what the caller
/// declared, not a deduction from `Δ_E`. Lemma 4.4 forbids the deduction.
///
/// Deliberately takes the [`LggrVerdict`] rather than a raw defect, so an
/// oracle-extracted reading cannot be laundered into a gate attribution.
pub fn gate_checklist(
    verdict: &LggrVerdict,
    declared: &[(OrganizationalGate, bool)],
) -> GateChecklistReading {
    match verdict {
        LggrVerdict::OracleExtractedUnsound { .. } => GateChecklistReading::NoSoundReading,
        LggrVerdict::GreenOracleNeeded { .. } | LggrVerdict::GreenNumericallySupported { .. } => {
            GateChecklistReading::ObservedZeroNotCertified
        }
        LggrVerdict::Red { .. } | LggrVerdict::PositiveGluingDefect { .. } => {
            let mut candidates: Vec<OrganizationalGate> = declared
                .iter()
                .filter(|(_, holds)| !*holds)
                .map(|(gate, _)| *gate)
                .collect();
            candidates.sort_unstable();
            candidates.dedup();
            let contradicts_declaration = candidates.is_empty();
            GateChecklistReading::SomeConditionFailed {
                candidates,
                contradicts_declaration,
            }
        }
    }
}

// ── LGGR III: EPK → CODA_GTLA overlay ─────────────────────────────────────────────

/// The six CODA_GTLA roles the EPK diagnostic surface maps onto (LGGR III).
///
/// The published stub returns these as a hardcoded `Dict[str, str]`; they are a
/// closed set, so they are typed here.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub enum CodaGtlaRole {
    /// Finite Obstruction — the defect ledger (Δ_E, Δ_P, Δ_C, Δ_R).
    Foc,
    /// Finite Descent — non-authoritative terminal policy receipts.
    Fda,
    /// Certified Transport — representation boundary loss exposure.
    Mur,
    /// Observer Relative — observer-dependent diagnostic metrics.
    Or,
    /// Finite Shadow — discrete trace sums without continuum limit.
    Cs,
    /// Residual Closure — refusal and audit feedback signals.
    A,
}

impl CodaGtlaRole {
    /// All six roles, in declared order.
    pub const ALL: [CodaGtlaRole; 6] = [
        CodaGtlaRole::Foc,
        CodaGtlaRole::Fda,
        CodaGtlaRole::Mur,
        CodaGtlaRole::Or,
        CodaGtlaRole::Cs,
        CodaGtlaRole::A,
    ];

    /// The short tag used in the published role map.
    pub fn tag(&self) -> &'static str {
        match self {
            Self::Foc => "FOC",
            Self::Fda => "FDA",
            Self::Mur => "MUR",
            Self::Or => "OR",
            Self::Cs => "CS",
            Self::A => "A",
        }
    }

    /// The declared EPK responsibility carried by this role.
    pub fn epk_responsibility(&self) -> &'static str {
        match self {
            Self::Foc => "Finite Obstruction - Defect Ledger (Delta_E, Delta_P, Delta_C, Delta_R)",
            Self::Fda => "Finite Descent - Non-authoritative terminal policy receipts",
            Self::Mur => "Certified Transport - Representation boundary loss exposure",
            Self::Or => "Observer Relative - Observer-dependent diagnostic metrics",
            Self::Cs => "Finite Shadow - Discrete trace sums without continuum limit",
            Self::A => "Residual Closure - Refusal & audit feedback signals",
        }
    }

    /// **Always** [`AuthorityEffect::None`], for every role.
    ///
    /// The overlay is a mapping of diagnostic responsibilities. No role in it mints
    /// authority — including `Fda`, whose receipts the paper marks
    /// non-authoritative by name.
    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
}
