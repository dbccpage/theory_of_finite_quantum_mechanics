
use serde::{Deserialize, Serialize};

use engine_types::authority::AuthorityEffect;

use crate::verdict::LggrVerdict;


#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub enum OrganizationalGate {
    GRep,
    GAuth,
    GTime,
    GEval,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum GRepReading {
    Weak,
    ProductSufficiency,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum GateSufficiencyStatus {
    RefutedByLemma44,
    CircularWithFactorization,
}

pub fn gate_sufficiency_status(reading: GRepReading) -> GateSufficiencyStatus {
    match reading {
        GRepReading::Weak => GateSufficiencyStatus::RefutedByLemma44,
        GRepReading::ProductSufficiency => GateSufficiencyStatus::CircularWithFactorization,
    }
}

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
    pub fn weak_g_rep_holds(&self) -> bool {
        self.representation[2] == self.global_pass
    }

    pub fn factorization_holds(&self) -> bool {
        self.global_pass == (self.local_left_pass && self.local_right_pass)
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct BoundaryOwner {
    pub name: String,
    pub has_authority: bool,
    pub has_accountability: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ClosureEligibility {
    RequiredFieldPresent,
    NoDeclaredOwner,
    OwnerLacksAuthority,
    OwnerLacksAccountability,
    OwnerLacksAuthorityAndAccountability,
}

impl ClosureEligibility {
    pub fn required_field_present(&self) -> bool {
        matches!(self, Self::RequiredFieldPresent)
    }

    pub fn certifies_closure(&self) -> bool {
        false
    }
}

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

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum GateChecklistReading {
    SomeConditionFailed {
        candidates: Vec<OrganizationalGate>,
        contradicts_declaration: bool,
    },
    ObservedZeroNotCertified,
    NoSoundReading,
}

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


#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub enum CodaGtlaRole {
    Foc,
    Fda,
    Mur,
    Or,
    Cs,
    A,
}

impl CodaGtlaRole {
    pub const ALL: [CodaGtlaRole; 6] = [
        CodaGtlaRole::Foc,
        CodaGtlaRole::Fda,
        CodaGtlaRole::Mur,
        CodaGtlaRole::Or,
        CodaGtlaRole::Cs,
        CodaGtlaRole::A,
    ];

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

    pub fn authority_effect(&self) -> AuthorityEffect {
        AuthorityEffect::None
    }
}
