
use super::cat_functor::{Category, DeclaredFiniteFunctor};
use super::finite_category::DeclaredFiniteCategory;
use super::validation::{
    ValidationLocation, ValidationReport, ValidationSeverity, ValidationUnit, ValidationViolation,
};
use std::collections::BTreeMap;


pub trait Monad {
    type C: Category;

    fn map_object(&self, x: &<Self::C as Category>::Ob) -> <Self::C as Category>::Ob;

    fn map_morphism(&self, f: &<Self::C as Category>::Mor) -> <Self::C as Category>::Mor;

    fn unit(&self, x: &<Self::C as Category>::Ob) -> <Self::C as Category>::Mor;

    fn multiply(&self, x: &<Self::C as Category>::Ob) -> <Self::C as Category>::Mor;
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredFiniteMonad {
    pub name: String,
    pub category: String,
    pub object_map: BTreeMap<String, String>,
    pub morphism_map: BTreeMap<String, String>,
    pub unit_components: BTreeMap<String, String>,
    pub multiplication_components: BTreeMap<String, String>,
}

impl DeclaredFiniteMonad {
    pub fn new(name: &str, category: &str) -> Self {
        Self {
            name: name.into(),
            category: category.into(),
            object_map: BTreeMap::new(),
            morphism_map: BTreeMap::new(),
            unit_components: BTreeMap::new(),
            multiplication_components: BTreeMap::new(),
        }
    }

    pub fn set_object_map(&mut self, src: &str, tgt: &str) {
        self.object_map.insert(src.into(), tgt.into());
    }

    pub fn set_morphism_map(&mut self, src: &str, tgt: &str) {
        self.morphism_map.insert(src.into(), tgt.into());
    }

    pub fn set_unit(&mut self, object: &str, morphism: &str) {
        self.unit_components.insert(object.into(), morphism.into());
    }

    pub fn set_multiply(&mut self, object: &str, morphism: &str) {
        self.multiplication_components
            .insert(object.into(), morphism.into());
    }

    pub fn underlying_functor(&self) -> DeclaredFiniteFunctor {
        let mut f =
            DeclaredFiniteFunctor::new(&format!("T_{}", self.name), &self.category, &self.category);
        f.object_map = self.object_map.clone();
        f.morphism_map = self.morphism_map.clone();
        f
    }
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProfunctorMonad {
    pub name: String,
    pub carrier_profunctor: String,
    pub unit_components: BTreeMap<String, String>,
    pub multiplication_components: BTreeMap<String, String>,
}

impl ProfunctorMonad {
    pub fn new(name: &str, carrier: &str) -> Self {
        Self {
            name: name.into(),
            carrier_profunctor: carrier.into(),
            unit_components: BTreeMap::new(),
            multiplication_components: BTreeMap::new(),
        }
    }
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ValidatedFiniteMonad(DeclaredFiniteMonad);

impl ValidatedFiniteMonad {
    pub fn try_new(
        monad: DeclaredFiniteMonad,
        category: &DeclaredFiniteCategory,
    ) -> Result<Self, ValidationReport> {
        let mut report = ValidationReport::new(&monad.name);

        if monad.category != category.name {
            report.add_violation(ValidationViolation::new(
                ValidationUnit::Other("Monad::CategoryMismatch".into()),
                ValidationLocation::Global,
                format!(
                    "Monad declared on {}, but category is {}",
                    monad.category, category.name
                ),
                ValidationSeverity::Error,
            ));
            return Err(report);
        }

        let functor = monad.underlying_functor();
        let functor_report =
            super::functor_composition::validate_functor_between(&functor, category, category);
        for violation in functor_report.typed_violations {
            report.add_violation(violation);
        }

        check_boundaries_and_naturality(&monad, category, &mut report);

        let left_units = check_left_unit(&monad, &category.compositions, &category.identities);
        for err in left_units {
            report.add_violation(ValidationViolation::new(
                ValidationUnit::Other("Monad::UnitLeft".into()),
                ValidationLocation::Global,
                err,
                ValidationSeverity::Error,
            ));
        }

        let right_units = check_right_unit(&monad, &category.compositions, &category.identities);
        for err in right_units {
            report.add_violation(ValidationViolation::new(
                ValidationUnit::Other("Monad::UnitRight".into()),
                ValidationLocation::Global,
                err,
                ValidationSeverity::Error,
            ));
        }

        let assoc = check_associativity(&monad, &category.compositions);
        for err in assoc {
            report.add_violation(ValidationViolation::new(
                ValidationUnit::Other("Monad::Associativity".into()),
                ValidationLocation::Global,
                err,
                ValidationSeverity::Error,
            ));
        }

        if report.all_passed() {
            Ok(Self(monad))
        } else {
            Err(report)
        }
    }

    pub fn declared(&self) -> &DeclaredFiniteMonad {
        &self.0
    }
}


fn check_boundaries_and_naturality(
    monad: &DeclaredFiniteMonad,
    category: &DeclaredFiniteCategory,
    report: &mut ValidationReport,
) {
    for obj in &category.objects {
        if let Some(eta_a) = monad.unit_components.get(obj) {
            if let Some(mor) = category.morphisms.get(eta_a) {
                let ta = monad.object_map.get(obj).unwrap_or(obj);
                if &mor.source != obj || &mor.target != ta {
                    report.add_violation(ValidationViolation::new(
                        ValidationUnit::Other("Monad::UnitBoundary".into()),
                        ValidationLocation::Object(obj.clone()),
                        format!(
                            "η_{} boundary is {} → {} instead of {} → {}",
                            obj, mor.source, mor.target, obj, ta
                        ),
                        ValidationSeverity::Error,
                    ));
                }
            } else {
                report.add_violation(ValidationViolation::new(
                    ValidationUnit::Other("Monad::UnitBoundary".into()),
                    ValidationLocation::Object(obj.clone()),
                    format!("η_{} refers to non-existent morphism {}", obj, eta_a),
                    ValidationSeverity::Error,
                ));
            }
        } else {
            report.add_violation(ValidationViolation::new(
                ValidationUnit::Other("Monad::UnitBoundary".into()),
                ValidationLocation::Object(obj.clone()),
                format!("Missing η_{}", obj),
                ValidationSeverity::Error,
            ));
        }

        let ta = monad.object_map.get(obj).cloned().unwrap_or_default();
        let tta = monad.object_map.get(&ta).cloned().unwrap_or_default();
        if let Some(mu_a) = monad.multiplication_components.get(obj) {
            if let Some(mor) = category.morphisms.get(mu_a) {
                if mor.source != tta || mor.target != ta {
                    report.add_violation(ValidationViolation::new(
                        ValidationUnit::Other("Monad::MultiplyBoundary".into()),
                        ValidationLocation::Object(obj.clone()),
                        format!(
                            "μ_{} boundary is {} → {} instead of {} → {}",
                            obj, mor.source, mor.target, tta, ta
                        ),
                        ValidationSeverity::Error,
                    ));
                }
            } else {
                report.add_violation(ValidationViolation::new(
                    ValidationUnit::Other("Monad::MultiplyBoundary".into()),
                    ValidationLocation::Object(obj.clone()),
                    format!("μ_{} refers to non-existent morphism {}", obj, mu_a),
                    ValidationSeverity::Error,
                ));
            }
        } else {
            report.add_violation(ValidationViolation::new(
                ValidationUnit::Other("Monad::MultiplyBoundary".into()),
                ValidationLocation::Object(obj.clone()),
                format!("Missing μ_{}", obj),
                ValidationSeverity::Error,
            ));
        }
    }

    for (f_name, mor) in &category.morphisms {
        let a = &mor.source;
        let b = &mor.target;

        let tf = monad.morphism_map.get(f_name).cloned().unwrap_or_default();
        let ttf = monad.morphism_map.get(&tf).cloned().unwrap_or_default();

        let eta_a = monad.unit_components.get(a).cloned().unwrap_or_default();
        let eta_b = monad.unit_components.get(b).cloned().unwrap_or_default();

        let mu_a = monad
            .multiplication_components
            .get(a)
            .cloned()
            .unwrap_or_default();
        let mu_b = monad
            .multiplication_components
            .get(b)
            .cloned()
            .unwrap_or_default();

        let left_eta = category.compositions.get(&(eta_a.clone(), tf.clone()));
        let right_eta = category.compositions.get(&(f_name.clone(), eta_b.clone()));

        if left_eta != right_eta {
            report.add_violation(ValidationViolation::new(
                ValidationUnit::Other("Monad::UnitNaturality".into()),
                ValidationLocation::Morphism(f_name.clone()),
                format!(
                    "Unit naturality failed at f={}: T(f)∘η_A = {:?}, η_B∘f = {:?}",
                    f_name, left_eta, right_eta
                ),
                ValidationSeverity::Error,
            ));
        }

        let left_mu = category.compositions.get(&(mu_a.clone(), tf.clone()));
        let right_mu = category.compositions.get(&(ttf.clone(), mu_b.clone()));

        if left_mu != right_mu {
            report.add_violation(ValidationViolation::new(
                ValidationUnit::Other("Monad::MultiplyNaturality".into()),
                ValidationLocation::Morphism(f_name.clone()),
                format!(
                    "Multiply naturality failed at f={}: T(f)∘μ_A = {:?}, μ_B∘T²(f) = {:?}",
                    f_name, left_mu, right_mu
                ),
                ValidationSeverity::Error,
            ));
        }
    }
}


pub fn check_left_unit(
    monad: &DeclaredFiniteMonad,
    compositions: &BTreeMap<(String, String), String>,
    identity_map: &BTreeMap<String, String>,
) -> Vec<String> {
    let mut violations = Vec::new();

    for (a, ta) in &monad.object_map {
        let Some(eta_a) = monad.unit_components.get(a) else {
            continue;
        };
        let Some(t_eta_a) = monad.morphism_map.get(eta_a.as_str()) else {
            continue;
        };
        let Some(mu_a) = monad.multiplication_components.get(a) else {
            continue;
        };

        let key = (t_eta_a.clone(), mu_a.clone());
        let composed = compositions.get(&key);
        let id_ta = identity_map.get(ta);

        match (composed, id_ta) {
            (Some(c), Some(id)) if c == id => {}
            (Some(c), Some(id)) => {
                violations.push(format!(
                    "Left unit at {}: μ ∘ T(η) = {} but id_{{T({})}} = {}",
                    a, c, a, id
                ));
            }
            _ => {
                violations.push(format!(
                    "Left unit at {}: composition or identity not defined",
                    a
                ));
            }
        }
    }

    violations
}

pub fn check_right_unit(
    monad: &DeclaredFiniteMonad,
    compositions: &BTreeMap<(String, String), String>,
    identity_map: &BTreeMap<String, String>,
) -> Vec<String> {
    let mut violations = Vec::new();

    for (a, ta) in &monad.object_map {
        let Some(eta_ta) = monad.unit_components.get(ta.as_str()) else {
            continue;
        };
        let Some(mu_a) = monad.multiplication_components.get(a) else {
            continue;
        };

        let key = (eta_ta.clone(), mu_a.clone());
        let composed = compositions.get(&key);
        let id_ta = identity_map.get(ta);

        match (composed, id_ta) {
            (Some(c), Some(id)) if c == id => {}
            (Some(c), Some(id)) => {
                violations.push(format!(
                    "Right unit at {}: μ ∘ η_T = {} but id_{{T({})}} = {}",
                    a, c, a, id
                ));
            }
            _ => {
                violations.push(format!(
                    "Right unit at {}: composition or identity not defined",
                    a
                ));
            }
        }
    }

    violations
}

pub fn check_associativity(
    monad: &DeclaredFiniteMonad,
    compositions: &BTreeMap<(String, String), String>,
) -> Vec<String> {
    let mut violations = Vec::new();

    for (a, ta) in &monad.object_map {
        let Some(mu_a) = monad.multiplication_components.get(a) else {
            continue;
        };
        let Some(t_mu_a) = monad.morphism_map.get(mu_a.as_str()) else {
            continue;
        };
        let Some(mu_ta) = monad.multiplication_components.get(ta.as_str()) else {
            continue;
        };

        let left_key = (t_mu_a.clone(), mu_a.clone());
        let left = compositions.get(&left_key);

        let right_key = (mu_ta.clone(), mu_a.clone());
        let right = compositions.get(&right_key);

        match (left, right) {
            (Some(l), Some(r)) if l == r => {}
            (Some(l), Some(r)) => {
                violations.push(format!("Assoc at {}: μ∘Tμ = {} but μ∘μT = {}", a, l, r));
            }
            _ => {
                violations.push(format!(
                    "Assoc at {}: one or both compositions not defined",
                    a
                ));
            }
        }
    }

    violations
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::finite_category_builder::DeclaredFiniteCategoryBuilder;

    fn make_identity_category() -> DeclaredFiniteCategory {
        DeclaredFiniteCategoryBuilder::new("C")
            .object("A")
            .identity("A", "id_A")
            .identity_compositions()
            .build()
    }

    fn make_identity_monad() -> DeclaredFiniteMonad {
        let mut m = DeclaredFiniteMonad::new("Id", "C");
        m.set_object_map("A", "A");
        m.set_morphism_map("id_A", "id_A");
        m.set_unit("A", "id_A");
        m.set_multiply("A", "id_A");
        m
    }

    #[test]
    fn identity_monad_validates() {
        let cat = make_identity_category();
        let m = make_identity_monad();

        let validated = ValidatedFiniteMonad::try_new(m, &cat);
        assert!(validated.is_ok(), "{:?}", validated.err());
    }

    #[test]
    fn missing_unit_is_violation() {
        let mut m = DeclaredFiniteMonad::new("Bad", "C");
        m.set_object_map("A", "A");

        let cat = make_identity_category();
        let validated = ValidatedFiniteMonad::try_new(m, &cat);
        assert!(validated.is_err());
    }
}
