//! Admitted finite strict 2-categories. AuthorityEffect: None.
//!
//! Convention: every table entry (a,b) composes a first, then b. Admission
//! checks the underlying 1-category, the disjoint union of hom categories,
//! globularity, exact horizontal domain/boundaries, strict associativity and
//! units, horizontal identity preservation and interchange:
//! h(v(a,b),v(c,d)) = v(h(a,c),h(b,d)).
//! The immutable wrapper owns both category certificates and the full tables.
//! Unknown identifiers return typed errors. A checked work bound is admitted
//! before any quadratic/cubic/quartic law enumeration; no unbounded-size or
//! weak/bicategorical coherence claim is made.

use super::finite_category::{DeclaredFiniteCategory, DeclaredMorphism, ValidatedFiniteCategory};
use std::collections::{BTreeMap, BTreeSet};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TwoCategoryLaw {
    ResourceBudget,
    OneCategory,
    VerticalCategory,
    Globularity,
    HorizontalDomain,
    HorizontalBoundary,
    HorizontalIdentities,
    HorizontalUnits,
    HorizontalAssociativity,
    Interchange,
    UnknownObject,
    UnknownOneMorphism,
    UnknownTwoMorphism,
    ComposabilityOne,
    ComposabilityVertical,
    ComposabilityHorizontal,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidationViolation {
    pub law: TwoCategoryLaw,
    pub message: String,
}
impl std::fmt::Display for ValidationViolation {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "[{:?}] {}", self.law, self.message)
    }
}
impl std::error::Error for ValidationViolation {}
fn violation(law: TwoCategoryLaw, message: impl Into<String>) -> ValidationViolation {
    ValidationViolation {
        law,
        message: message.into(),
    }
}

/// Fallible boundary queries admit caller-supplied identifiers explicitly.
/// Implementing this trait alone does not confer an admission certificate.
pub trait TwoCategory {
    type Ob: Clone + Eq + std::fmt::Debug;
    type OneMor: Clone + Eq + std::fmt::Debug;
    type TwoMor: Clone + Eq + std::fmt::Debug;
    fn source_1(&self, f: &Self::OneMor) -> Result<Self::Ob, ValidationViolation>;
    fn target_1(&self, f: &Self::OneMor) -> Result<Self::Ob, ValidationViolation>;
    fn source_2(&self, a: &Self::TwoMor) -> Result<Self::OneMor, ValidationViolation>;
    fn target_2(&self, a: &Self::TwoMor) -> Result<Self::OneMor, ValidationViolation>;
    fn id_1(&self, a: &Self::Ob) -> Result<Self::OneMor, ValidationViolation>;
    fn id_2(&self, f: &Self::OneMor) -> Result<Self::TwoMor, ValidationViolation>;
    fn compose_1(
        &self,
        f: &Self::OneMor,
        g: &Self::OneMor,
    ) -> Result<Self::OneMor, ValidationViolation>;
    fn compose_2_vertical(
        &self,
        a: &Self::TwoMor,
        b: &Self::TwoMor,
    ) -> Result<Self::TwoMor, ValidationViolation>;
    fn compose_2_horizontal(
        &self,
        a: &Self::TwoMor,
        b: &Self::TwoMor,
    ) -> Result<Self::TwoMor, ValidationViolation>;
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredOneMorphism {
    pub name: String,
    pub source: String,
    pub target: String,
}
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredTwoMorphism {
    pub name: String,
    pub source: String,
    pub target: String,
}

/// Untrusted finite tables. Public mutability is confined to candidates.
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

/// Default cap on a conservative count of enumerated law tuples. Label copying
/// and ordered-map comparisons additionally depend on total input bytes.
pub const DEFAULT_LAW_WORK_LIMIT: usize = 1_000_000;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidatedFiniteTwoCategory {
    declared: DeclaredFiniteTwoCategory,
    underlying: ValidatedFiniteCategory,
    vertical: ValidatedFiniteCategory,
}
impl ValidatedFiniteTwoCategory {
    pub fn try_new(declared: DeclaredFiniteTwoCategory) -> Result<Self, Vec<ValidationViolation>> {
        Self::try_new_with_limit(declared, DEFAULT_LAW_WORK_LIMIT)
    }
    pub fn try_new_with_limit(
        declared: DeclaredFiniteTwoCategory,
        limit: usize,
    ) -> Result<Self, Vec<ValidationViolation>> {
        Self::admit(declared, limit).map_err(|err| vec![err])
    }
    fn admit(
        declared: DeclaredFiniteTwoCategory,
        limit: usize,
    ) -> Result<Self, ValidationViolation> {
        check_work_budget(&declared, limit)?;
        let underlying = admit_underlying(&declared)?;
        check_globularity(&declared)?;
        let vertical = admit_vertical(&declared)?;
        let candidate = Self {
            declared,
            underlying,
            vertical,
        };
        candidate.check_horizontal_laws()?;
        Ok(candidate)
    }
    pub fn declared(&self) -> &DeclaredFiniteTwoCategory {
        &self.declared
    }
    pub fn underlying(&self) -> &ValidatedFiniteCategory {
        &self.underlying
    }
    /// A disjoint union of hom categories: its objects are all 1-morphisms and
    /// its arrows all 2-morphisms. Globularity separates the hom components.
    pub fn vertical_category(&self) -> &ValidatedFiniteCategory {
        &self.vertical
    }

    fn one(&self, name: &str) -> Result<&DeclaredOneMorphism, ValidationViolation> {
        self.declared
            .one_morphisms
            .get(name)
            .ok_or_else(|| violation(TwoCategoryLaw::UnknownOneMorphism, name))
    }
    fn two(&self, name: &str) -> Result<&DeclaredTwoMorphism, ValidationViolation> {
        self.declared
            .two_morphisms
            .get(name)
            .ok_or_else(|| violation(TwoCategoryLaw::UnknownTwoMorphism, name))
    }
    fn horizontal_seam(&self, a: &str, b: &str) -> Option<(&str, &str)> {
        let a = self.declared.two_morphisms.get(a)?;
        let b = self.declared.two_morphisms.get(b)?;
        let f = self.declared.one_morphisms.get(&a.source)?;
        let g = self.declared.one_morphisms.get(&b.source)?;
        Some((&f.target, &g.source))
    }
    fn horizontally_composable(&self, a: &str, b: &str) -> bool {
        self.horizontal_seam(a, b).is_some_and(|(x, y)| x == y)
    }
    fn check_horizontal_laws(&self) -> Result<(), ValidationViolation> {
        self.check_horizontal_domain()?;
        self.check_horizontal_boundaries()?;
        self.check_horizontal_identities()?;
        self.check_horizontal_units()?;
        self.check_horizontal_associativity()?;
        self.check_interchange()?;
        Ok(())
    }
    fn check_horizontal_domain(&self) -> Result<(), ValidationViolation> {
        let c = &self.declared;
        for a in c.two_morphisms.keys() {
            for b in c.two_morphisms.keys() {
                let present = c.compose_2_horizontal.contains_key(&(a.clone(), b.clone()));
                if present != self.horizontally_composable(a, b) {
                    return Err(violation(
                        TwoCategoryLaw::HorizontalDomain,
                        format!("{a} then {b}"),
                    ));
                }
            }
        }
        for (a, b) in c.compose_2_horizontal.keys() {
            if !self.horizontally_composable(a, b) {
                return Err(violation(
                    TwoCategoryLaw::HorizontalDomain,
                    format!("extraneous {a} then {b}"),
                ));
            }
        }
        Ok(())
    }
    fn check_horizontal_boundaries(&self) -> Result<(), ValidationViolation> {
        for ((a, b), result) in &self.declared.compose_2_horizontal {
            self.check_horizontal_boundary(a, b, result)?;
        }
        Ok(())
    }
    fn check_horizontal_boundary(
        &self,
        a: &str,
        b: &str,
        result: &str,
    ) -> Result<(), ValidationViolation> {
        let a = self.two(a)?;
        let b = self.two(b)?;
        let result = self.two(result)?;
        let source = self.compose_1(&a.source, &b.source)?;
        let target = self.compose_1(&a.target, &b.target)?;
        if result.source != source || result.target != target {
            return Err(violation(TwoCategoryLaw::HorizontalBoundary, &result.name));
        }
        Ok(())
    }
    fn check_horizontal_identities(&self) -> Result<(), ValidationViolation> {
        for ((f, g), result) in &self.declared.compose_1 {
            self.horizontal_identity_at(f, g, result)?;
        }
        Ok(())
    }
    fn horizontal_identity_at(
        &self,
        f: &str,
        g: &str,
        result: &str,
    ) -> Result<(), ValidationViolation> {
        let first = self.id_2(&f.into())?;
        let second = self.id_2(&g.into())?;
        let left = self.compose_2_horizontal(&first, &second)?;
        let right = self.id_2(&result.into())?;
        if left != right {
            return Err(violation(
                TwoCategoryLaw::HorizontalIdentities,
                format!("{f} then {g}"),
            ));
        }
        Ok(())
    }
    fn check_horizontal_units(&self) -> Result<(), ValidationViolation> {
        for a in self.declared.two_morphisms.keys() {
            self.horizontal_unit_at(a)?;
        }
        Ok(())
    }
    fn object_identity_two(&self, object: &str) -> Result<String, ValidationViolation> {
        self.id_2(&self.id_1(&object.into())?)
    }
    fn horizontal_unit_at(&self, a: &str) -> Result<(), ValidationViolation> {
        let arrow = self.two(a)?;
        let source = self.one(&arrow.source)?;
        let first = self.object_identity_two(&source.source)?;
        let second = self.object_identity_two(&source.target)?;
        let left = self.compose_2_horizontal(&first, &a.into())?;
        let right = self.compose_2_horizontal(&a.into(), &second)?;
        if left != a || right != a {
            return Err(violation(TwoCategoryLaw::HorizontalUnits, a));
        }
        Ok(())
    }
    fn check_horizontal_associativity(&self) -> Result<(), ValidationViolation> {
        for (a, b) in self.declared.compose_2_horizontal.keys() {
            for c in self.declared.two_morphisms.keys() {
                if self.horizontally_composable(b, c) {
                    horizontal_associativity_at(self, a, b, c)?;
                }
            }
        }
        Ok(())
    }
    fn check_interchange(&self) -> Result<(), ValidationViolation> {
        for (a, b) in self.declared.compose_2_vertical.keys() {
            for (c, d) in self.declared.compose_2_vertical.keys() {
                if self.horizontally_composable(a, c) {
                    check_interchange_law(self, a, b, c, d)?;
                }
            }
        }
        Ok(())
    }
}

fn checked_work_term(
    count: usize,
    power: u32,
    factor: usize,
) -> Result<usize, ValidationViolation> {
    count
        .checked_pow(power)
        .and_then(|n| n.checked_mul(factor))
        .ok_or_else(|| violation(TwoCategoryLaw::ResourceBudget, "law-work bound overflow"))
}
fn law_work_upper_bound(c: &DeclaredFiniteTwoCategory) -> Result<usize, ValidationViolation> {
    let m = c.one_morphisms.len();
    let n = c.two_morphisms.len();
    let v = c.compose_2_vertical.len();
    let mut total = 0usize;
    // One-category pairs/triples, vertical pairs/triples, horizontal domain,
    // horizontal triples, identities and all pairs of vertical table entries.
    for (count, power, factor) in [(m, 3, 1), (m, 2, 2), (n, 3, 2), (n, 2, 4), (v, 2, 1)] {
        total = total
            .checked_add(checked_work_term(count, power, factor)?)
            .ok_or_else(|| violation(TwoCategoryLaw::ResourceBudget, "law-work sum overflow"))?;
    }
    for count in [
        c.objects.len(),
        m,
        n,
        c.id_1.len(),
        c.id_2.len(),
        c.compose_1.len(),
        v,
        c.compose_2_horizontal.len(),
    ] {
        total = total.checked_add(count).ok_or_else(|| {
            violation(TwoCategoryLaw::ResourceBudget, "record-count sum overflow")
        })?;
    }
    Ok(total)
}
fn check_work_budget(
    c: &DeclaredFiniteTwoCategory,
    limit: usize,
) -> Result<(), ValidationViolation> {
    let needed = law_work_upper_bound(c)?;
    if needed > limit {
        return Err(violation(
            TwoCategoryLaw::ResourceBudget,
            format!("work bound {needed} exceeds limit {limit}"),
        ));
    }
    Ok(())
}
fn admit_underlying(
    c: &DeclaredFiniteTwoCategory,
) -> Result<ValidatedFiniteCategory, ValidationViolation> {
    let raw = DeclaredFiniteCategory {
        name: c.name.clone(),
        objects: c.objects.clone(),
        morphisms: c
            .one_morphisms
            .iter()
            .map(|(key, m)| {
                (
                    key.clone(),
                    DeclaredMorphism::new(&m.name, &m.source, &m.target),
                )
            })
            .collect(),
        identities: c.id_1.clone(),
        compositions: c.compose_1.clone(),
    };
    ValidatedFiniteCategory::try_new(raw)
        .map_err(|report| violation(TwoCategoryLaw::OneCategory, format!("{report:?}")))
}
fn admit_vertical(
    c: &DeclaredFiniteTwoCategory,
) -> Result<ValidatedFiniteCategory, ValidationViolation> {
    let raw = DeclaredFiniteCategory {
        name: format!("{}.hom-disjoint-union", c.name),
        objects: c.one_morphisms.keys().cloned().collect(),
        morphisms: c
            .two_morphisms
            .iter()
            .map(|(key, m)| {
                (
                    key.clone(),
                    DeclaredMorphism::new(&m.name, &m.source, &m.target),
                )
            })
            .collect(),
        identities: c.id_2.clone(),
        compositions: c.compose_2_vertical.clone(),
    };
    ValidatedFiniteCategory::try_new(raw)
        .map_err(|report| violation(TwoCategoryLaw::VerticalCategory, format!("{report:?}")))
}
fn check_globularity(c: &DeclaredFiniteTwoCategory) -> Result<(), ValidationViolation> {
    for a in c.two_morphisms.values() {
        globularity_at(c, a)?;
    }
    Ok(())
}
fn globularity_at(
    c: &DeclaredFiniteTwoCategory,
    a: &DeclaredTwoMorphism,
) -> Result<(), ValidationViolation> {
    let f = c
        .one_morphisms
        .get(&a.source)
        .ok_or_else(|| violation(TwoCategoryLaw::Globularity, &a.name))?;
    let g = c
        .one_morphisms
        .get(&a.target)
        .ok_or_else(|| violation(TwoCategoryLaw::Globularity, &a.name))?;
    if f.source != g.source || f.target != g.target {
        return Err(violation(TwoCategoryLaw::Globularity, &a.name));
    }
    Ok(())
}

impl TwoCategory for ValidatedFiniteTwoCategory {
    type Ob = String;
    type OneMor = String;
    type TwoMor = String;
    fn source_1(&self, f: &String) -> Result<String, ValidationViolation> {
        Ok(self.one(f)?.source.clone())
    }
    fn target_1(&self, f: &String) -> Result<String, ValidationViolation> {
        Ok(self.one(f)?.target.clone())
    }
    fn source_2(&self, a: &String) -> Result<String, ValidationViolation> {
        Ok(self.two(a)?.source.clone())
    }
    fn target_2(&self, a: &String) -> Result<String, ValidationViolation> {
        Ok(self.two(a)?.target.clone())
    }
    fn id_1(&self, a: &String) -> Result<String, ValidationViolation> {
        self.declared
            .id_1
            .get(a)
            .cloned()
            .ok_or_else(|| violation(TwoCategoryLaw::UnknownObject, a))
    }
    fn id_2(&self, f: &String) -> Result<String, ValidationViolation> {
        self.declared
            .id_2
            .get(f)
            .cloned()
            .ok_or_else(|| violation(TwoCategoryLaw::UnknownOneMorphism, f))
    }
    fn compose_1(&self, f: &String, g: &String) -> Result<String, ValidationViolation> {
        lookup_composition(
            &self.declared.compose_1,
            f,
            g,
            TwoCategoryLaw::ComposabilityOne,
        )
    }
    fn compose_2_vertical(&self, a: &String, b: &String) -> Result<String, ValidationViolation> {
        lookup_composition(
            &self.declared.compose_2_vertical,
            a,
            b,
            TwoCategoryLaw::ComposabilityVertical,
        )
    }
    fn compose_2_horizontal(&self, a: &String, b: &String) -> Result<String, ValidationViolation> {
        lookup_composition(
            &self.declared.compose_2_horizontal,
            a,
            b,
            TwoCategoryLaw::ComposabilityHorizontal,
        )
    }
}
fn lookup_composition(
    table: &BTreeMap<(String, String), String>,
    a: &str,
    b: &str,
    law: TwoCategoryLaw,
) -> Result<String, ValidationViolation> {
    table
        .get(&(a.into(), b.into()))
        .cloned()
        .ok_or_else(|| violation(law, format!("{a} then {b}")))
}

pub fn check_vertical_composable<C: TwoCategory>(
    cat: &C,
    a: &C::TwoMor,
    b: &C::TwoMor,
) -> Result<(), ValidationViolation> {
    if cat.target_2(a)? != cat.source_2(b)? {
        return Err(violation(
            TwoCategoryLaw::ComposabilityVertical,
            format!("{a:?} then {b:?}"),
        ));
    }
    Ok(())
}
fn two_object_boundary<C: TwoCategory>(
    cat: &C,
    a: &C::TwoMor,
) -> Result<(C::Ob, C::Ob), ValidationViolation> {
    let f = cat.source_2(a)?;
    let g = cat.target_2(a)?;
    let source = cat.source_1(&f)?;
    let target = cat.target_1(&f)?;
    if (source.clone(), target.clone()) != (cat.source_1(&g)?, cat.target_1(&g)?) {
        return Err(violation(TwoCategoryLaw::Globularity, format!("{a:?}")));
    }
    Ok((source, target))
}
pub fn check_horizontal_composable<C: TwoCategory>(
    cat: &C,
    a: &C::TwoMor,
    b: &C::TwoMor,
) -> Result<(), ValidationViolation> {
    let (_, target) = two_object_boundary(cat, a)?;
    let (source, _) = two_object_boundary(cat, b)?;
    if target != source {
        return Err(violation(
            TwoCategoryLaw::ComposabilityHorizontal,
            format!("{a:?} then {b:?}"),
        ));
    }
    Ok(())
}
fn horizontal_associativity_at<C: TwoCategory>(
    cat: &C,
    a: &C::TwoMor,
    b: &C::TwoMor,
    c: &C::TwoMor,
) -> Result<(), ValidationViolation> {
    let left = cat.compose_2_horizontal(&cat.compose_2_horizontal(a, b)?, c)?;
    let right = cat.compose_2_horizontal(a, &cat.compose_2_horizontal(b, c)?)?;
    if left != right {
        return Err(violation(
            TwoCategoryLaw::HorizontalAssociativity,
            format!("{a:?}, {b:?}, {c:?}"),
        ));
    }
    Ok(())
}
fn check_square_boundary<C: TwoCategory>(
    cat: &C,
    a: &C::TwoMor,
    b: &C::TwoMor,
    c: &C::TwoMor,
    d: &C::TwoMor,
) -> Result<(), ValidationViolation> {
    check_vertical_composable(cat, a, b)?;
    check_vertical_composable(cat, c, d)?;
    check_horizontal_composable(cat, a, c)?;
    check_horizontal_composable(cat, b, d)?;
    Ok(())
}
fn interchange_values<C: TwoCategory>(
    cat: &C,
    a: &C::TwoMor,
    b: &C::TwoMor,
    c: &C::TwoMor,
    d: &C::TwoMor,
) -> Result<(C::TwoMor, C::TwoMor), ValidationViolation> {
    let ab = cat.compose_2_vertical(a, b)?;
    let cd = cat.compose_2_vertical(c, d)?;
    let left = cat.compose_2_horizontal(&ab, &cd)?;
    let ac = cat.compose_2_horizontal(a, c)?;
    let bd = cat.compose_2_horizontal(b, d)?;
    let right = cat.compose_2_vertical(&ac, &bd)?;
    Ok((left, right))
}
/// First-then-second convention: h(v(a,b),v(c,d)) = v(h(a,c),h(b,d)).
pub fn check_interchange_law<C: TwoCategory>(
    cat: &C,
    a: &C::TwoMor,
    b: &C::TwoMor,
    c: &C::TwoMor,
    d: &C::TwoMor,
) -> Result<(), ValidationViolation> {
    check_square_boundary(cat, a, b, c, d)?;
    let (left, right) = interchange_values(cat, a, b, c, d)?;
    if left != right {
        return Err(violation(
            TwoCategoryLaw::Interchange,
            format!("{left:?} versus {right:?}"),
        ));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn scalar_two_category() -> DeclaredFiniteTwoCategory {
        let mut c = DeclaredFiniteTwoCategory::new("C2 scalars");
        c.objects.insert("*".into());
        c.one_morphisms.insert(
            "e".into(),
            DeclaredOneMorphism {
                name: "e".into(),
                source: "*".into(),
                target: "*".into(),
            },
        );
        c.id_1.insert("*".into(), "e".into());
        c.compose_1.insert(("e".into(), "e".into()), "e".into());
        for i in 0..2 {
            c.two_morphisms.insert(
                i.to_string(),
                DeclaredTwoMorphism {
                    name: i.to_string(),
                    source: "e".into(),
                    target: "e".into(),
                },
            );
        }
        c.id_2.insert("e".into(), "0".into());
        for i in 0..2 {
            for j in 0..2 {
                let pair = (i.to_string(), j.to_string());
                c.compose_2_vertical
                    .insert(pair.clone(), ((i + j) % 2).to_string());
                c.compose_2_horizontal
                    .insert(pair, ((i + j) % 2).to_string());
            }
        }
        c
    }

    #[test]
    fn rejects_empty_admission_mechanism_and_broken_unit_tables() {
        let base = scalar_two_category();
        assert!(ValidatedFiniteTwoCategory::try_new(base.clone()).is_ok());
        let mut cases = Vec::new();
        let mut c = base.clone();
        c.id_1.clear();
        cases.push(c);
        let mut c = base.clone();
        c.id_2.clear();
        cases.push(c);
        let mut c = base.clone();
        c.compose_1.clear();
        cases.push(c);
        let mut c = base.clone();
        c.compose_2_vertical.remove(&("0".into(), "1".into()));
        cases.push(c);
        let mut c = base.clone();
        c.compose_2_horizontal.remove(&("0".into(), "1".into()));
        cases.push(c);
        let mut c = base.clone();
        c.name.clear();
        cases.push(c);
        let mut c = base.clone();
        c.two_morphisms.get_mut("1").unwrap().name = "other".into();
        cases.push(c);
        let mut c = base.clone();
        c.one_morphisms.get_mut("e").unwrap().source = "outside".into();
        cases.push(c);
        let mut c = base;
        c.compose_2_horizontal
            .insert(("outside".into(), "0".into()), "0".into());
        cases.push(c);
        for (i, c) in cases.into_iter().enumerate() {
            assert!(
                ValidatedFiniteTwoCategory::try_new(c).is_err(),
                "malformed case {i}"
            );
        }
    }

    #[test]
    fn unknown_identifier_lookups_are_typed_failures_instead_of_panics() {
        let c = ValidatedFiniteTwoCategory::try_new(scalar_two_category()).unwrap();
        let outside = "outside".to_string();
        assert!(std::panic::catch_unwind(|| c.source_1(&outside)).is_ok());
        assert!(std::panic::catch_unwind(|| c.target_1(&outside)).is_ok());
        assert!(std::panic::catch_unwind(|| c.source_2(&outside)).is_ok());
        assert!(std::panic::catch_unwind(|| c.target_2(&outside)).is_ok());
        assert!(std::panic::catch_unwind(|| c.id_1(&outside)).is_ok());
        assert!(std::panic::catch_unwind(|| c.id_2(&outside)).is_ok());
        assert_eq!(
            c.source_1(&outside).unwrap_err().law,
            TwoCategoryLaw::UnknownOneMorphism
        );
        assert_eq!(
            c.target_1(&outside).unwrap_err().law,
            TwoCategoryLaw::UnknownOneMorphism
        );
        assert_eq!(
            c.source_2(&outside).unwrap_err().law,
            TwoCategoryLaw::UnknownTwoMorphism
        );
        assert_eq!(
            c.target_2(&outside).unwrap_err().law,
            TwoCategoryLaw::UnknownTwoMorphism
        );
        assert_eq!(
            c.id_1(&outside).unwrap_err().law,
            TwoCategoryLaw::UnknownObject
        );
        assert_eq!(
            c.id_2(&outside).unwrap_err().law,
            TwoCategoryLaw::UnknownOneMorphism
        );
        assert!(c.compose_1(&outside, &outside).is_err());
        assert!(c.compose_2_vertical(&outside, &outside).is_err());
        assert!(c.compose_2_horizontal(&outside, &outside).is_err());
        assert!(check_vertical_composable(&c, &outside, &outside).is_err());
        assert!(check_horizontal_composable(&c, &outside, &outside).is_err());
        assert!(check_interchange_law(&c, &outside, &outside, &outside, &outside).is_err());
    }

    fn scalar_tables(v: &[[usize; 3]; 3], h: &[[usize; 3]; 3]) -> DeclaredFiniteTwoCategory {
        let mut c = scalar_two_category();
        c.name = "three scalar cells".into();
        c.two_morphisms.insert(
            "2".into(),
            DeclaredTwoMorphism {
                name: "2".into(),
                source: "e".into(),
                target: "e".into(),
            },
        );
        for i in 0..3 {
            for j in 0..3 {
                let pair = (i.to_string(), j.to_string());
                c.compose_2_vertical
                    .insert(pair.clone(), v[i][j].to_string());
                c.compose_2_horizontal.insert(pair, h[i][j].to_string());
            }
        }
        c
    }

    fn unital_table(mut code: usize) -> [[usize; 3]; 3] {
        let mut result = [[0; 3]; 3];
        for i in 0..3 {
            result[0][i] = i;
            result[i][0] = i;
        }
        for row in result.iter_mut().skip(1) {
            for value in row.iter_mut().skip(1) {
                *value = code % 3;
                code /= 3;
            }
        }
        result
    }

    fn associative(table: &[[usize; 3]; 3]) -> bool {
        for a in 0..3 {
            for b in 0..3 {
                for c in 0..3 {
                    if table[table[a][b]][c] != table[a][table[b][c]] {
                        return false;
                    }
                }
            }
        }
        true
    }
    fn commutative(table: &[[usize; 3]; 3]) -> bool {
        (0..3).all(|i| (0..3).all(|j| table[i][j] == table[j][i]))
    }

    #[test]
    fn all_6561_unital_scalar_pairs_match_eckmann_hilton() {
        let mut admitted = 0;
        for v in 0..81 {
            let vertical = unital_table(v);
            for h in 0..81 {
                let horizontal = unital_table(h);
                // Independent theorem basis: two unital operations obeying
                // interchange coincide and form one commutative monoid.
                let expected =
                    vertical == horizontal && associative(&vertical) && commutative(&vertical);
                let checked =
                    ValidatedFiniteTwoCategory::try_new(scalar_tables(&vertical, &horizontal));
                assert_eq!(checked.is_ok(), expected, "vertical {v}, horizontal {h}");
                admitted += usize::from(checked.is_ok());
            }
        }
        assert!(admitted > 1); // includes groups and non-invertible monoids
    }

    fn locally_discrete(base: &DeclaredFiniteCategory) -> DeclaredFiniteTwoCategory {
        let mut c = DeclaredFiniteTwoCategory::new("locally discrete");
        c.objects = base.objects.clone();
        c.id_1 = base.identities.clone();
        c.compose_1 = base.compositions.clone();
        for (name, f) in &base.morphisms {
            c.one_morphisms.insert(
                name.clone(),
                DeclaredOneMorphism {
                    name: name.clone(),
                    source: f.source.clone(),
                    target: f.target.clone(),
                },
            );
            let identity = format!("I({name})");
            c.two_morphisms.insert(
                identity.clone(),
                DeclaredTwoMorphism {
                    name: identity.clone(),
                    source: name.clone(),
                    target: name.clone(),
                },
            );
            c.id_2.insert(name.clone(), identity.clone());
            c.compose_2_vertical
                .insert((identity.clone(), identity.clone()), identity);
        }
        for ((f, g), result) in &base.compositions {
            c.compose_2_horizontal.insert(
                (format!("I({f})"), format!("I({g})")),
                format!("I({result})"),
            );
        }
        c
    }

    #[test]
    fn object_and_one_cell_boundaries_and_owned_context_are_exact() {
        let base = crate::finite_category_builder::DeclaredFiniteCategoryBuilder::walking_arrow(
            "C", "A", "B", "f",
        )
        .build();
        let mut raw = locally_discrete(&base);
        let c = ValidatedFiniteTwoCategory::try_new(raw.clone()).unwrap();
        raw.objects.clear();
        raw.two_morphisms.clear();
        assert_eq!(c.source_1(&"f".into()).unwrap(), "A");
        assert_eq!(c.target_1(&"f".into()).unwrap(), "B");
        assert_eq!(
            c.underlying().declared(),
            &DeclaredFiniteCategory {
                name: "locally discrete".into(),
                ..base.clone()
            }
        );
        assert_eq!(c.vertical_category().declared().objects.len(), 3);
        assert!(check_horizontal_composable(&c, &"I(id_A)".into(), &"I(f)".into()).is_ok());
        assert!(check_horizontal_composable(&c, &"I(f)".into(), &"I(id_A)".into()).is_err());
        assert!(check_vertical_composable(&c, &"I(f)".into(), &"I(id_A)".into()).is_err());
        let mut bad = locally_discrete(&base);
        bad.two_morphisms.get_mut("I(f)").unwrap().target = "id_A".into();
        assert_eq!(
            ValidatedFiniteTwoCategory::try_new(bad).unwrap_err()[0].law,
            TwoCategoryLaw::Globularity
        );
        let mut extra = locally_discrete(&base);
        extra
            .compose_2_horizontal
            .insert(("I(f)".into(), "I(id_A)".into()), "I(f)".into());
        assert_eq!(
            ValidatedFiniteTwoCategory::try_new(extra).unwrap_err()[0].law,
            TwoCategoryLaw::HorizontalDomain
        );
        let mut wrong_boundary = locally_discrete(&base);
        wrong_boundary
            .compose_2_horizontal
            .insert(("I(id_A)".into(), "I(f)".into()), "I(id_B)".into());
        assert_eq!(
            ValidatedFiniteTwoCategory::try_new(wrong_boundary).unwrap_err()[0].law,
            TwoCategoryLaw::HorizontalBoundary
        );
    }

    /// One object, two 1-cells e (unit) and f (absorbing); automorphisms
    /// of f are C3, e has only its identity. Tensor on f,f is p*a+q*b.
    fn two_color_linear_tensor(p: usize, q: usize, left_unit: bool) -> DeclaredFiniteTwoCategory {
        let mut c = DeclaredFiniteTwoCategory::new("two color tensor");
        c.objects.insert("*".into());
        c.id_1.insert("*".into(), "e".into());
        for f in ["e", "f"] {
            c.one_morphisms.insert(
                f.into(),
                DeclaredOneMorphism {
                    name: f.into(),
                    source: "*".into(),
                    target: "*".into(),
                },
            );
        }
        for a in ["e", "f"] {
            for b in ["e", "f"] {
                c.compose_1.insert(
                    (a.into(), b.into()),
                    if a == "e" && b == "e" { "e" } else { "f" }.into(),
                );
            }
        }
        let cells = [
            ("e0", "e", 0),
            ("f0", "f", 0),
            ("f1", "f", 1),
            ("f2", "f", 2),
        ];
        for (name, f, _) in cells {
            c.two_morphisms.insert(
                name.into(),
                DeclaredTwoMorphism {
                    name: name.into(),
                    source: f.into(),
                    target: f.into(),
                },
            );
        }
        c.id_2.insert("e".into(), "e0".into());
        c.id_2.insert("f".into(), "f0".into());
        for (a, f, x) in cells {
            for (b, g, y) in cells {
                let key = (a.into(), b.into());
                if f == g {
                    c.compose_2_vertical.insert(
                        key.clone(),
                        if f == "e" {
                            "e0".into()
                        } else {
                            format!("f{}", (x + y) % 3)
                        },
                    );
                }
                let h = match (f, g) {
                    ("e", "e") => "e0".into(),
                    ("e", _) => {
                        if left_unit {
                            b.into()
                        } else {
                            "f0".into()
                        }
                    }
                    (_, "e") => a.into(),
                    _ => format!("f{}", (p * x + q * y) % 3),
                };
                c.compose_2_horizontal.insert(key, h);
            }
        }
        c
    }

    #[test]
    fn associativity_and_strict_units_have_independent_counterexamples() {
        assert!(ValidatedFiniteTwoCategory::try_new(two_color_linear_tensor(1, 1, true)).is_ok());
        let nonassoc = two_color_linear_tensor(2, 1, true);
        assert_eq!(
            ValidatedFiniteTwoCategory::try_new(nonassoc).unwrap_err()[0].law,
            TwoCategoryLaw::HorizontalAssociativity
        );
        let bad_unit = two_color_linear_tensor(0, 0, false);
        assert_eq!(
            ValidatedFiniteTwoCategory::try_new(bad_unit).unwrap_err()[0].law,
            TwoCategoryLaw::HorizontalUnits
        );
    }

    #[test]
    fn horizontal_identity_preservation_is_not_just_interchange() {
        let mut c = two_color_linear_tensor(0, 0, true);
        c.two_morphisms.remove("f2");
        c.compose_2_vertical
            .retain(|(a, b), _| a != "f2" && b != "f2");
        c.compose_2_horizontal
            .retain(|(a, b), _| a != "f2" && b != "f2");
        // Aut(f) is the two-element idempotent monoid. Tensor(f,f) is
        // constant at its nonidentity idempotent: composition preserving,
        // associative and strictly unital at e, but not identity preserving.
        for a in 0..2 {
            for b in 0..2 {
                c.compose_2_vertical
                    .insert((format!("f{a}"), format!("f{b}")), format!("f{}", a.max(b)));
                c.compose_2_horizontal
                    .insert((format!("f{a}"), format!("f{b}")), "f1".into());
            }
        }
        assert_eq!(
            ValidatedFiniteTwoCategory::try_new(c).unwrap_err()[0].law,
            TwoCategoryLaw::HorizontalIdentities
        );
    }

    #[test]
    fn work_budget_is_checked_before_enumeration_and_has_exact_boundaries() {
        let raw = scalar_two_category();
        let needed = law_work_upper_bound(&raw).unwrap();
        assert_eq!(needed, 66); // 1+2+16+16+16 law tuples, plus 15 table records
        assert!(ValidatedFiniteTwoCategory::try_new_with_limit(raw.clone(), needed).is_ok());
        assert_eq!(
            ValidatedFiniteTwoCategory::try_new_with_limit(raw, needed - 1).unwrap_err()[0].law,
            TwoCategoryLaw::ResourceBudget
        );
        assert_eq!(
            checked_work_term(usize::MAX, 3, 1).unwrap_err().law,
            TwoCategoryLaw::ResourceBudget
        );
        assert_eq!(
            checked_work_term(usize::MAX, 1, 2).unwrap_err().law,
            TwoCategoryLaw::ResourceBudget
        );
    }
}
