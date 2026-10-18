
use super::cat_functor::{CatFunctor, Category, DeclaredFiniteFunctor};
use super::functor_composition::validate_functor_between;
use std::collections::BTreeMap;


pub trait UpFunctor: CatFunctor {}

pub trait ForgetFunctor: CatFunctor {}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ForgetResult<Base, Evidence> {
    pub base: Base,
    pub evidence: Evidence,
}

pub trait ForgetFunctorWithEvidence: ForgetFunctor {
    type Lifted;
    type Base;
    type Evidence;

    fn forget(x: Self::Lifted) -> ForgetResult<Self::Base, Self::Evidence>;
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ForgetKind {
    Projection,
    Structure,
}


pub trait AdjunctionPair {
    type Base: Category;
    type Lifted: Category;
    type Left: CatFunctor<Source = Self::Base, Target = Self::Lifted>;
    type Right: CatFunctor<Source = Self::Lifted, Target = Self::Base>;

    type Unit;
    type Counit;
}

pub use super::finite_category::{DeclaredFiniteCategory, DeclaredMorphism};


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredFiniteAdjunction {
    pub name: String,
    pub left_functor: String,
    pub right_functor: String,
    pub left: DeclaredFiniteFunctor,
    pub right: DeclaredFiniteFunctor,
    pub left_ob_map: BTreeMap<String, String>,
    pub left_mor_map: BTreeMap<String, String>,
    pub right_ob_map: BTreeMap<String, String>,
    pub right_mor_map: BTreeMap<String, String>,
    pub unit_components: BTreeMap<String, String>,
    pub counit_components: BTreeMap<String, String>,
}

impl DeclaredFiniteAdjunction {
    pub fn new(name: &str, left: &str, right: &str) -> Self {
        Self {
            name: name.into(),
            left_functor: left.into(),
            right_functor: right.into(),
            left: DeclaredFiniteFunctor::new(left, "", ""),
            right: DeclaredFiniteFunctor::new(right, "", ""),
            left_ob_map: BTreeMap::new(),
            left_mor_map: BTreeMap::new(),
            right_ob_map: BTreeMap::new(),
            right_mor_map: BTreeMap::new(),
            unit_components: BTreeMap::new(),
            counit_components: BTreeMap::new(),
        }
    }

    pub fn new_between(
        name: &str,
        base: &str,
        lifted: &str,
        left_name: &str,
        right_name: &str,
    ) -> Self {
        let mut adj = Self::new(name, left_name, right_name);
        adj.left.source_category = base.into();
        adj.left.target_category = lifted.into();
        adj.right.source_category = lifted.into();
        adj.right.target_category = base.into();
        adj
    }

    pub fn set_left_ob(&mut self, src: &str, tgt: &str) {
        self.left.map_object(src, tgt);
        self.left_ob_map.insert(src.into(), tgt.into());
    }
    pub fn set_left_mor(&mut self, src: &str, tgt: &str) {
        self.left.map_morphism(src, tgt);
        self.left_mor_map.insert(src.into(), tgt.into());
    }
    pub fn set_right_ob(&mut self, src: &str, tgt: &str) {
        self.right.map_object(src, tgt);
        self.right_ob_map.insert(src.into(), tgt.into());
    }
    pub fn set_right_mor(&mut self, src: &str, tgt: &str) {
        self.right.map_morphism(src, tgt);
        self.right_mor_map.insert(src.into(), tgt.into());
    }
    pub fn set_unit(&mut self, object: &str, morphism: &str) {
        self.unit_components.insert(object.into(), morphism.into());
    }
    pub fn set_counit(&mut self, object: &str, morphism: &str) {
        self.counit_components
            .insert(object.into(), morphism.into());
    }
}


#[derive(Debug, Clone)]
pub struct DerivedMonad {
    pub name: String,
    pub t_ob_map: BTreeMap<String, String>,
    pub t_mor_map: BTreeMap<String, String>,
    pub unit: BTreeMap<String, String>,
    pub multiply: BTreeMap<String, String>,
}

impl DerivedMonad {
    pub fn from_adjunction(adj: &DeclaredFiniteAdjunction) -> Self {
        let mut t_ob_map = BTreeMap::new();
        let mut t_mor_map = BTreeMap::new();
        let mut multiply = BTreeMap::new();

        for (a, la) in &adj.left.object_map {
            if let Some(rla) = adj.right.on_object(la) {
                t_ob_map.insert(a.clone(), rla.into());
            }
        }

        for (f, lf) in &adj.left.morphism_map {
            if let Some(rlf) = adj.right.on_morphism(lf) {
                t_mor_map.insert(f.clone(), rlf.into());
            }
        }

        for (a, la) in &adj.left.object_map {
            if let Some(eps_la) = adj.counit_components.get(la) {
                if let Some(r_eps_la) = adj.right.on_morphism(eps_la) {
                    multiply.insert(a.clone(), r_eps_la.into());
                }
            }
        }

        DerivedMonad {
            name: format!("T_{}_{}", adj.right.name, adj.left.name),
            t_ob_map,
            t_mor_map,
            unit: adj.unit_components.clone(),
            multiply,
        }
    }
}


#[derive(Debug, Clone)]
pub struct DerivedComonad {
    pub name: String,
    pub d_ob_map: BTreeMap<String, String>,
    pub d_mor_map: BTreeMap<String, String>,
    pub counit: BTreeMap<String, String>,
    pub comultiply: BTreeMap<String, String>,
}

impl DerivedComonad {
    pub fn from_adjunction(adj: &DeclaredFiniteAdjunction) -> Self {
        let mut d_ob_map = BTreeMap::new();
        let mut d_mor_map = BTreeMap::new();
        let mut comultiply = BTreeMap::new();

        for (b, rb) in &adj.right.object_map {
            if let Some(lrb) = adj.left.on_object(rb) {
                d_ob_map.insert(b.clone(), lrb.into());
            }
        }

        for (g, rg) in &adj.right.morphism_map {
            if let Some(lrg) = adj.left.on_morphism(rg) {
                d_mor_map.insert(g.clone(), lrg.into());
            }
        }

        for (b, rb) in &adj.right_ob_map {
            if let Some(eta_rb) = adj.unit_components.get(rb) {
                if let Some(l_eta_rb) = adj.left_mor_map.get(eta_rb) {
                    comultiply.insert(b.clone(), l_eta_rb.clone());
                }
            }
        }

        DerivedComonad {
            name: format!("D_{}_{}", adj.left_functor, adj.right_functor),
            d_ob_map,
            d_mor_map,
            counit: adj.counit_components.clone(),
            comultiply,
        }
    }
}


pub fn kleisli_compose(
    monad: &DerivedMonad,
    f_result: &str,
    g: &str,
    c: &str,
    base_compositions: &BTreeMap<(String, String), String>,
) -> Result<String, String> {
    let t_g = monad
        .t_mor_map
        .get(g)
        .ok_or_else(|| format!("Kleisli: T({}) not defined", g))?;

    let key1 = (f_result.to_string(), t_g.clone());
    let tg_f = base_compositions
        .get(&key1)
        .ok_or_else(|| format!("Kleisli: T({}) ∘ {} not in composition table", g, f_result))?;

    let mu_c = monad
        .multiply
        .get(c)
        .ok_or_else(|| format!("Kleisli: μ_{} not defined", c))?;

    let key2 = (tg_f.clone(), mu_c.clone());
    let result = base_compositions.get(&key2).ok_or_else(|| {
        format!(
            "Kleisli: μ_{} ∘ (T({}) ∘ {}) not in composition table",
            c, g, f_result
        )
    })?;

    Ok(result.clone())
}


use super::validation::{
    AdjunctionValidation, ValidationLocation, ValidationReport, ValidationSeverity, ValidationUnit,
    ValidationViolation,
};

fn adjunction_violation(
    unit: AdjunctionValidation,
    location: ValidationLocation,
    message: impl Into<String>,
) -> ValidationViolation {
    ValidationViolation::new(
        ValidationUnit::Adjunction(unit),
        location,
        message,
        ValidationSeverity::Error,
    )
}

pub fn validate_declared_adjunction(
    adj: &DeclaredFiniteAdjunction,
    base: &DeclaredFiniteCategory,
    lifted: &DeclaredFiniteCategory,
) -> ValidationReport {
    let mut report = ValidationReport::new(&adj.name);
    let mut left = adj.left.clone();
    left.name = adj.left_functor.clone();
    left.source_category = base.name.clone();
    left.target_category = lifted.name.clone();
    left.object_map = adj.left_ob_map.clone();
    left.morphism_map = adj.left_mor_map.clone();

    let mut right = adj.right.clone();
    right.name = adj.right_functor.clone();
    right.source_category = lifted.name.clone();
    right.target_category = base.name.clone();
    right.object_map = adj.right_ob_map.clone();
    right.morphism_map = adj.right_mor_map.clone();

    let left_report = validate_functor_between(&left, base, lifted);
    for res in left_report.results {
        report.add(res);
    }
    for violation in left_report.typed_violations {
        report.add_violation(violation);
    }

    let right_report = validate_functor_between(&right, lifted, base);
    for res in right_report.results {
        report.add(res);
    }
    for violation in right_report.typed_violations {
        report.add_violation(violation);
    }

    let mut tl_violations = Vec::new();
    for a in base.object_names() {
        let Some(la) = left.on_object(a) else {
            continue;
        };
        let Some(eta_a) = adj.unit_components.get(a) else {
            tl_violations.push(adjunction_violation(
                AdjunctionValidation::TriangleLeft,
                ValidationLocation::Object(a.into()),
                format!("η_{} not defined", a),
            ));
            continue;
        };
        let Some(l_eta_a) = left.on_morphism(eta_a) else {
            continue;
        };
        let Some(eps_la) = adj.counit_components.get(la) else {
            continue;
        };

        let composed = lifted.compose(l_eta_a, eps_la);
        let id_la = lifted.identity_of(la);

        match (composed, id_la) {
            (Some(c), Some(i)) if c == i => {}
            (Some(c), Some(i)) => {
                tl_violations.push(adjunction_violation(
                    AdjunctionValidation::TriangleLeft,
                    ValidationLocation::Object(a.into()),
                    format!(
                        "ε_{{L({})}} ∘ L(η_{}) = {} ≠ id_{{L({})}} = {}",
                        a, a, c, a, i
                    ),
                ));
            }
            _ => tl_violations.push(adjunction_violation(
                AdjunctionValidation::TriangleLeft,
                ValidationLocation::Object(a.into()),
                format!(
                    "ε_{{L({})}} ∘ L(η_{}) not defined or identity missing",
                    a, a
                ),
            )),
        }
    }
    report.add_typed("triangle_left", tl_violations);

    let mut tr_violations = Vec::new();
    for b in lifted.object_names() {
        let Some(rb) = right.on_object(b) else {
            continue;
        };
        let Some(eps_b) = adj.counit_components.get(b) else {
            tr_violations.push(adjunction_violation(
                AdjunctionValidation::TriangleRight,
                ValidationLocation::Object(b.into()),
                format!("ε_{} not defined", b),
            ));
            continue;
        };
        let Some(r_eps_b) = right.on_morphism(eps_b) else {
            continue;
        };
        let Some(eta_rb) = adj.unit_components.get(rb) else {
            continue;
        };

        let composed = base.compose(eta_rb, r_eps_b);
        let id_rb = base.identity_of(rb);

        match (composed, id_rb) {
            (Some(c), Some(i)) if c == i => {}
            (Some(c), Some(i)) => {
                tr_violations.push(adjunction_violation(
                    AdjunctionValidation::TriangleRight,
                    ValidationLocation::Object(b.into()),
                    format!(
                        "R(ε_{}) ∘ η_{{R({})}} = {} ≠ id_{{R({})}} = {}",
                        b, b, c, b, i
                    ),
                ));
            }
            _ => tr_violations.push(adjunction_violation(
                AdjunctionValidation::TriangleRight,
                ValidationLocation::Object(b.into()),
                format!(
                    "R(ε_{}) ∘ η_{{R({})}} not defined or identity missing",
                    b, b
                ),
            )),
        }
    }
    report.add_typed("triangle_right", tr_violations);

    report
}


pub fn check_derived_monad_left_unit(
    monad: &DerivedMonad,
    base_compositions: &BTreeMap<(String, String), String>,
    base_ids: &BTreeMap<String, String>,
) -> Vec<String> {
    let mut violations = Vec::new();
    for (a, ta) in &monad.t_ob_map {
        let Some(eta_a) = monad.unit.get(a) else {
            continue;
        };
        let Some(t_eta_a) = monad.t_mor_map.get(eta_a.as_str()) else {
            violations.push(format!("Monad left unit: T(η_{}) not defined", a));
            continue;
        };
        let Some(mu_a) = monad.multiply.get(a) else {
            violations.push(format!("Monad left unit: μ_{} not defined", a));
            continue;
        };
        let key = (t_eta_a.clone(), mu_a.clone());
        let composed = base_compositions.get(&key);
        let id_ta = base_ids.get(ta);
        match (composed, id_ta) {
            (Some(c), Some(i)) if c == i => {}
            (Some(c), Some(i)) => violations.push(format!(
                "Monad left unit at {}: μ∘T(η) = {} ≠ id_T = {}",
                a, c, i
            )),
            _ => violations.push(format!(
                "Monad left unit at {}: composition or identity not defined",
                a
            )),
        }
    }
    violations
}

pub fn check_derived_monad_right_unit(
    monad: &DerivedMonad,
    base_compositions: &BTreeMap<(String, String), String>,
    base_ids: &BTreeMap<String, String>,
) -> Vec<String> {
    let mut violations = Vec::new();
    for (a, ta) in &monad.t_ob_map {
        let Some(eta_ta) = monad.unit.get(ta.as_str()) else {
            continue;
        };
        let Some(mu_a) = monad.multiply.get(a) else {
            continue;
        };
        let key = (eta_ta.clone(), mu_a.clone());
        let composed = base_compositions.get(&key);
        let id_ta = base_ids.get(ta);
        match (composed, id_ta) {
            (Some(c), Some(i)) if c == i => {}
            (Some(c), Some(i)) => violations.push(format!(
                "Monad right unit at {}: μ∘ηT = {} ≠ id_T = {}",
                a, c, i
            )),
            _ => violations.push(format!("Monad right unit at {}: not defined", a)),
        }
    }
    violations
}


pub fn check_derived_monad_associativity(
    monad: &DerivedMonad,
    base_compositions: &BTreeMap<(String, String), String>,
) -> Vec<String> {
    let mut violations = Vec::new();
    for (a, ta) in &monad.t_ob_map {
        let Some(_tta) = monad.t_ob_map.get(ta) else {
            continue;
        };

        let Some(mu_a) = monad.multiply.get(a) else {
            continue;
        };
        let Some(mu_ta) = monad.multiply.get(ta) else {
            continue;
        };
        let Some(t_mu_a) = monad.t_mor_map.get(mu_a) else {
            continue;
        };

        let lhs_key = (t_mu_a.clone(), mu_a.clone());
        let lhs = base_compositions.get(&lhs_key);

        let rhs_key = (mu_ta.clone(), mu_a.clone());
        let rhs = base_compositions.get(&rhs_key);

        match (lhs, rhs) {
            (Some(l), Some(r)) if l == r => {}
            (Some(l), Some(r)) => violations.push(format!(
                "Monad associativity at {}: μ∘T(μ) = {} ≠ μ∘μ_T = {}",
                a, l, r
            )),
            _ => violations.push(format!(
                "Monad associativity at {}: compositions not defined",
                a
            )),
        }
    }
    violations
}

pub fn check_derived_comonad_left_counit(
    comonad: &DerivedComonad,
    lifted_compositions: &BTreeMap<(String, String), String>,
    lifted_ids: &BTreeMap<String, String>,
) -> Vec<String> {
    let mut violations = Vec::new();
    for (b, db) in &comonad.d_ob_map {
        let Some(delta_b) = comonad.comultiply.get(b) else {
            continue;
        };
        let Some(eps_db) = comonad.counit.get(db) else {
            continue;
        };

        let key = (delta_b.clone(), eps_db.clone());
        let composed = lifted_compositions.get(&key);
        let id_db = lifted_ids.get(db);
        match (composed, id_db) {
            (Some(c), Some(i)) if c == i => {}
            (Some(c), Some(i)) => violations.push(format!(
                "Comonad left counit at {}: εD∘δ = {} ≠ id_D = {}",
                b, c, i
            )),
            _ => violations.push(format!("Comonad left counit at {}: not defined", b)),
        }
    }
    violations
}

pub fn check_derived_comonad_right_counit(
    comonad: &DerivedComonad,
    lifted_compositions: &BTreeMap<(String, String), String>,
    lifted_ids: &BTreeMap<String, String>,
) -> Vec<String> {
    let mut violations = Vec::new();
    for (b, db) in &comonad.d_ob_map {
        let Some(delta_b) = comonad.comultiply.get(b) else {
            continue;
        };
        let Some(eps_b) = comonad.counit.get(b) else {
            continue;
        };
        let Some(d_eps_b) = comonad.d_mor_map.get(eps_b) else {
            continue;
        };

        let key = (delta_b.clone(), d_eps_b.clone());
        let composed = lifted_compositions.get(&key);
        let id_db = lifted_ids.get(db);
        match (composed, id_db) {
            (Some(c), Some(i)) if c == i => {}
            (Some(c), Some(i)) => violations.push(format!(
                "Comonad right counit at {}: Dε∘δ = {} ≠ id_D = {}",
                b, c, i
            )),
            _ => violations.push(format!("Comonad right counit at {}: not defined", b)),
        }
    }
    violations
}

pub fn check_derived_comonad_coassociativity(
    comonad: &DerivedComonad,
    lifted_compositions: &BTreeMap<(String, String), String>,
) -> Vec<String> {
    let mut violations = Vec::new();
    for (b, db) in &comonad.d_ob_map {
        let Some(_ddb) = comonad.d_ob_map.get(db) else {
            continue;
        };

        let Some(delta_b) = comonad.comultiply.get(b) else {
            continue;
        };
        let Some(delta_db) = comonad.comultiply.get(db) else {
            continue;
        };
        let Some(d_delta_b) = comonad.d_mor_map.get(delta_b) else {
            continue;
        };

        let lhs_key = (delta_b.clone(), delta_db.clone());
        let lhs = lifted_compositions.get(&lhs_key);

        let rhs_key = (delta_b.clone(), d_delta_b.clone());
        let rhs = lifted_compositions.get(&rhs_key);

        match (lhs, rhs) {
            (Some(l), Some(r)) if l == r => {}
            (Some(l), Some(r)) => violations.push(format!(
                "Comonad coassociativity at {}: δD∘δ = {} ≠ Dδ∘δ = {}",
                b, l, r
            )),
            _ => violations.push(format!(
                "Comonad coassociativity at {}: compositions not defined",
                b
            )),
        }
    }
    violations
}


#[cfg(test)]
mod tests {
    use super::*;

    fn trivial_adjunction() -> DeclaredFiniteAdjunction {
        let mut adj = DeclaredFiniteAdjunction::new("Trivial", "L", "R");
        adj.set_left_ob("*", "*'");
        adj.set_left_mor("id_*", "id_*'");
        adj.set_right_ob("*'", "*");
        adj.set_right_mor("id_*'", "id_*");
        adj.set_unit("*", "id_*");
        adj.set_counit("*'", "id_*'");
        adj.set_left_mor("id_*", "id_*'");
        adj
    }

    fn dummy_base_category() -> DeclaredFiniteCategory {
        let mut cat = DeclaredFiniteCategory::new("Base");
        cat.add_identity("*", "id_*");
        cat.set_composition("id_*", "id_*", "id_*");
        cat
    }

    fn dummy_lifted_category() -> DeclaredFiniteCategory {
        let mut cat = DeclaredFiniteCategory::new("Lifted");
        cat.add_identity("*'", "id_*'");
        cat.set_composition("id_*'", "id_*'", "id_*'");
        cat
    }

    #[test]
    fn left_triangle_trivial() {
        let adj = trivial_adjunction();
        let base = dummy_base_category();
        let lifted = dummy_lifted_category();
        let report = validate_declared_adjunction(&adj, &base, &lifted);
        assert!(
            report.all_passed(),
            "Should pass: {:?}",
            report.typed_violations
        );
    }

    #[test]
    fn derived_monad_from_trivial() {
        let adj = trivial_adjunction();
        let monad = DerivedMonad::from_adjunction(&adj);
        assert_eq!(monad.t_ob_map.get("*"), Some(&"*".to_string()));
        assert_eq!(monad.unit.get("*"), Some(&"id_*".to_string()));
    }

    #[test]
    fn derived_comonad_from_trivial() {
        let adj = trivial_adjunction();
        let comonad = DerivedComonad::from_adjunction(&adj);
        assert_eq!(comonad.d_ob_map.get("*'"), Some(&"*'".to_string()));
        assert_eq!(comonad.counit.get("*'"), Some(&"id_*'".to_string()));
    }

    #[test]
    fn derived_monad_left_unit_trivial() {
        let adj = trivial_adjunction();
        let monad = DerivedMonad::from_adjunction(&adj);
        let base_comp: BTreeMap<(String, String), String> =
            vec![(("id_*".into(), "id_*".into()), "id_*".into())]
                .into_iter()
                .collect();
        let base_ids: BTreeMap<String, String> =
            vec![("*".into(), "id_*".into())].into_iter().collect();
        let v = check_derived_monad_left_unit(&monad, &base_comp, &base_ids);
        assert!(v.is_empty(), "Monad left unit should pass: {:?}", v);
    }

    #[test]
    fn forget_result_construction() {
        let r = ForgetResult {
            base: 42,
            evidence: "dropped group law",
        };
        assert_eq!(r.base, 42);
        assert_eq!(ForgetKind::Structure, ForgetKind::Structure);
        assert_ne!(ForgetKind::Projection, ForgetKind::Structure);
    }

    #[test]
    fn missing_unit_is_violation() {
        let mut adj = DeclaredFiniteAdjunction::new_between("Bad", "Base", "Lifted", "L", "R");
        adj.set_left_ob("*", "*'");
        adj.set_left_mor("id_*", "id_*'");
        adj.set_right_ob("*'", "*");
        adj.set_right_mor("id_*'", "id_*");
        let base = dummy_base_category();
        let lifted = dummy_lifted_category();
        let report = validate_declared_adjunction(&adj, &base, &lifted);
        assert!(!report.all_passed());
        assert!(report
            .typed_violations
            .iter()
            .any(|v| v.unit == ValidationUnit::Adjunction(AdjunctionValidation::TriangleLeft)));
    }
}
