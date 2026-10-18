//! TwoCategory — Spec Section 10.
//!
//! A 2-category extends a category with a third layer:
//!   Objects, 1-morphisms (f: A → B), 2-morphisms (α: f ⇒ g).
//!
//! Laws (validation obligations, not compiler-enforced):
//!   - Associativity of ∘ (horizontal composition)
//!   - Unit laws for identities
//!   - Interchange law:
//!     (β ∘_v α) ∘_h (δ ∘_v γ) = (β ∘_h δ) ∘_v (α ∘_h γ)

use std::collections::{BTreeMap, BTreeSet};

// ---------------------------------------------------------------------------
// ValidationViolation
// ---------------------------------------------------------------------------

/// A validation violation from a 2-categorical law check.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidationViolation {
    pub law: String,
    pub message: String,
}

impl std::fmt::Display for ValidationViolation {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "[{}] {}", self.law, self.message)
    }
}

// ---------------------------------------------------------------------------
// Trait: TwoCategory
// ---------------------------------------------------------------------------

/// A (small) 2-category.
pub trait TwoCategory {
    type Ob: Clone + Eq + std::fmt::Debug;
    type OneMor: Clone + Eq + std::fmt::Debug;
    type TwoMor: Clone + Eq + std::fmt::Debug;

    fn source_1(&self, f: &Self::OneMor) -> Self::Ob;
    fn target_1(&self, f: &Self::OneMor) -> Self::Ob;

    fn source_2(&self, alpha: &Self::TwoMor) -> Self::OneMor;
    fn target_2(&self, alpha: &Self::TwoMor) -> Self::OneMor;

    fn id_1(&self, a: &Self::Ob) -> Self::OneMor;
    fn id_2(&self, f: &Self::OneMor) -> Self::TwoMor;

    /// Composition of 1-morphisms: g ∘ f.
    fn compose_1(
        &self,
        f: &Self::OneMor,
        g: &Self::OneMor,
    ) -> Result<Self::OneMor, ValidationViolation>;

    /// Vertical composition of 2-morphisms: β ∘_v α (same 1-morphism endpoints).
    fn compose_2_vertical(
        &self,
        alpha: &Self::TwoMor,
        beta: &Self::TwoMor,
    ) -> Result<Self::TwoMor, ValidationViolation>;

    /// Horizontal composition of 2-morphisms: β ∘_h α (sequential 1-morphisms).
    fn compose_2_horizontal(
        &self,
        alpha: &Self::TwoMor,
        beta: &Self::TwoMor,
    ) -> Result<Self::TwoMor, ValidationViolation>;
}

// ---------------------------------------------------------------------------
// Data Layer: Finite 2-Category
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredOneMorphism {
    pub name: String,
    pub source: String,
    pub target: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredTwoMorphism {
    pub name: String,
    pub source: String, // 1-morphism name
    pub target: String, // 1-morphism name
}

/// A declared finite 2-category (unvalidated).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredFiniteTwoCategory {
    pub name: String,
    pub objects: BTreeSet<String>,
    pub one_morphisms: BTreeMap<String, DeclaredOneMorphism>,
    pub two_morphisms: BTreeMap<String, DeclaredTwoMorphism>,

    pub id_1: BTreeMap<String, String>,
    pub id_2: BTreeMap<String, String>,

    pub compose_1: BTreeMap<(String, String), String>,
    pub compose_2_vertical: BTreeMap<(String, String), String>,
    pub compose_2_horizontal: BTreeMap<(String, String), String>,
}

impl DeclaredFiniteTwoCategory {
    pub fn new(name: &str) -> Self {
        Self {
            name: name.into(),
            objects: BTreeSet::new(),
            one_morphisms: BTreeMap::new(),
            two_morphisms: BTreeMap::new(),
            id_1: BTreeMap::new(),
            id_2: BTreeMap::new(),
            compose_1: BTreeMap::new(),
            compose_2_vertical: BTreeMap::new(),
            compose_2_horizontal: BTreeMap::new(),
        }
    }
}

/// A validated finite 2-category, wrapped after law checking.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidatedFiniteTwoCategory {
    declared: DeclaredFiniteTwoCategory,
}

impl ValidatedFiniteTwoCategory {
    pub fn try_new(declared: DeclaredFiniteTwoCategory) -> Result<Self, Vec<ValidationViolation>> {
        // Validate laws here
        // ... (Placeholder for full validation like finite_category)
        Ok(Self { declared })
    }

    pub fn declared(&self) -> &DeclaredFiniteTwoCategory {
        &self.declared
    }
}

impl TwoCategory for ValidatedFiniteTwoCategory {
    type Ob = String;
    type OneMor = String;
    type TwoMor = String;

    fn source_1(&self, f: &Self::OneMor) -> Self::Ob {
        self.declared.one_morphisms.get(f).unwrap().source.clone()
    }
    fn target_1(&self, f: &Self::OneMor) -> Self::Ob {
        self.declared.one_morphisms.get(f).unwrap().target.clone()
    }

    fn source_2(&self, alpha: &Self::TwoMor) -> Self::OneMor {
        self.declared
            .two_morphisms
            .get(alpha)
            .unwrap()
            .source
            .clone()
    }
    fn target_2(&self, alpha: &Self::TwoMor) -> Self::OneMor {
        self.declared
            .two_morphisms
            .get(alpha)
            .unwrap()
            .target
            .clone()
    }

    fn id_1(&self, a: &Self::Ob) -> Self::OneMor {
        self.declared.id_1.get(a).unwrap().clone()
    }
    fn id_2(&self, f: &Self::OneMor) -> Self::TwoMor {
        self.declared.id_2.get(f).unwrap().clone()
    }

    fn compose_1(
        &self,
        f: &Self::OneMor,
        g: &Self::OneMor,
    ) -> Result<Self::OneMor, ValidationViolation> {
        self.declared
            .compose_1
            .get(&(f.clone(), g.clone()))
            .cloned()
            .ok_or_else(|| ValidationViolation {
                law: "composability_1".into(),
                message: format!("1-morphisms not composable: {} then {}", f, g),
            })
    }

    fn compose_2_vertical(
        &self,
        alpha: &Self::TwoMor,
        beta: &Self::TwoMor,
    ) -> Result<Self::TwoMor, ValidationViolation> {
        self.declared
            .compose_2_vertical
            .get(&(alpha.clone(), beta.clone()))
            .cloned()
            .ok_or_else(|| ValidationViolation {
                law: "composability_2_vertical".into(),
                message: format!(
                    "2-morphisms not vertically composable: {} then {}",
                    alpha, beta
                ),
            })
    }

    fn compose_2_horizontal(
        &self,
        alpha: &Self::TwoMor,
        beta: &Self::TwoMor,
    ) -> Result<Self::TwoMor, ValidationViolation> {
        self.declared
            .compose_2_horizontal
            .get(&(alpha.clone(), beta.clone()))
            .cloned()
            .ok_or_else(|| ValidationViolation {
                law: "composability_2_horizontal".into(),
                message: format!(
                    "2-morphisms not horizontally composable: {} then {}",
                    alpha, beta
                ),
            })
    }
}

// ---------------------------------------------------------------------------
// Law checkers
// ---------------------------------------------------------------------------

pub fn check_vertical_composable<C: TwoCategory>(
    cat: &C,
    alpha: &C::TwoMor,
    beta: &C::TwoMor,
) -> Result<(), ValidationViolation> {
    if cat.target_2(alpha) == cat.source_2(beta) {
        Ok(())
    } else {
        Err(ValidationViolation {
            law: "vertical_composability".into(),
            message: format!(
                "2-morphisms are not vertically composable: {:?} then {:?}",
                alpha, beta
            ),
        })
    }
}

pub fn check_horizontal_composable<C: TwoCategory>(
    cat: &C,
    alpha: &C::TwoMor,
    gamma: &C::TwoMor,
) -> Result<(), ValidationViolation> {
    let f = cat.source_2(alpha);
    let g = cat.source_2(gamma);
    if cat.target_1(&f) == cat.source_1(&g) {
        Ok(())
    } else {
        Err(ValidationViolation {
            law: "horizontal_composability".into(),
            message: format!(
                "2-morphisms are not horizontally composable: {:?} then {:?}",
                alpha, gamma
            ),
        })
    }
}

/// Check the interchange law:
///   (β ∘_v α) ∘_h (δ ∘_v γ) = (β ∘_h δ) ∘_v (α ∘_h γ)
pub fn check_interchange_law<C: TwoCategory>(
    cat: &C,
    alpha: &C::TwoMor,
    beta: &C::TwoMor,
    gamma: &C::TwoMor,
    delta: &C::TwoMor,
) -> Result<(), ValidationViolation> {
    // Explicit boundary checks
    check_vertical_composable(cat, alpha, beta)?;
    check_vertical_composable(cat, gamma, delta)?;
    check_horizontal_composable(cat, alpha, gamma)?;
    check_horizontal_composable(cat, beta, delta)?;

    // Left side: (β ∘_v α) ∘_h (δ ∘_v γ)
    let beta_v_alpha = cat.compose_2_vertical(alpha, beta)?;
    let delta_v_gamma = cat.compose_2_vertical(gamma, delta)?;
    let left = cat.compose_2_horizontal(&beta_v_alpha, &delta_v_gamma)?;

    // Right side: (β ∘_h δ) ∘_v (α ∘_h γ)
    let beta_h_delta = cat.compose_2_horizontal(beta, delta)?;
    let alpha_h_gamma = cat.compose_2_horizontal(alpha, gamma)?;
    let right = cat.compose_2_vertical(&alpha_h_gamma, &beta_h_delta)?;

    if left == right {
        Ok(())
    } else {
        Err(ValidationViolation {
            law: "interchange".into(),
            message: format!("Interchange law failed: left {:?}, right {:?}", left, right),
        })
    }
}
