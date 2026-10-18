
use std::collections::BTreeMap;

pub type CompositionTable = BTreeMap<(String, String), String>;

pub trait CatFunctor {
    type Source: Category;
    type Target: Category;

    fn map_object(&self, object: &<Self::Source as Category>::Ob)
        -> <Self::Target as Category>::Ob;

    fn map_morphism(
        &self,
        morphism: &<Self::Source as Category>::Mor,
    ) -> <Self::Target as Category>::Mor;
}


pub trait ContravariantFunctor {
    type Source: Category;
    type Target: Category;

    fn map_object(&self, object: &<Self::Source as Category>::Ob)
        -> <Self::Target as Category>::Ob;

    fn map_morphism(
        &self,
        morphism: &<Self::Source as Category>::Mor,
    ) -> <Self::Target as Category>::Mor;
}


#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DeclaredFiniteFunctor {
    pub name: String,
    pub source_category: String,
    pub target_category: String,
    pub object_map: BTreeMap<String, String>,
    pub morphism_map: BTreeMap<String, String>,
}

impl DeclaredFiniteFunctor {
    pub fn new(name: &str, source: &str, target: &str) -> Self {
        Self {
            name: name.into(),
            source_category: source.into(),
            target_category: target.into(),
            object_map: BTreeMap::new(),
            morphism_map: BTreeMap::new(),
        }
    }

    pub fn map_object(&mut self, src: &str, tgt: &str) {
        self.object_map.insert(src.into(), tgt.into());
    }

    pub fn map_morphism(&mut self, src: &str, tgt: &str) {
        self.morphism_map.insert(src.into(), tgt.into());
    }

    pub fn on_object(&self, obj: &str) -> Option<&str> {
        self.object_map.get(obj).map(|s| s.as_str())
    }

    pub fn on_morphism(&self, mor: &str) -> Option<&str> {
        self.morphism_map.get(mor).map(|s| s.as_str())
    }
}


pub trait Category {
    type Ob: Clone + Eq + std::fmt::Debug;
    type Mor: Clone + Eq + std::fmt::Debug;

    fn id(&self, x: &Self::Ob) -> Self::Mor;
    fn src(&self, f: &Self::Mor) -> Self::Ob;
    fn tgt(&self, f: &Self::Mor) -> Self::Ob;
    fn compose(&self, f: &Self::Mor, g: &Self::Mor) -> Option<Self::Mor>;
}


pub fn check_identity_law(functor: &DeclaredFiniteFunctor) -> Vec<String> {
    let mut violations = Vec::new();
    for (src_obj, tgt_obj) in &functor.object_map {
        let src_id = format!("id_{}", src_obj);
        let expected_tgt_id = format!("id_{}", tgt_obj);
        match functor.morphism_map.get(&src_id) {
            Some(mapped) if mapped == &expected_tgt_id => {}
            Some(mapped) => {
                violations.push(format!(
                    "Identity law violated at {}: F(id_{}) = {} but expected {}",
                    src_obj, src_obj, mapped, expected_tgt_id
                ));
            }
            None => {
                violations.push(format!("Identity law: F(id_{}) is not defined", src_obj));
            }
        }
    }
    violations
}

pub fn check_composition_law(
    functor: &DeclaredFiniteFunctor,
    source_compositions: &[(&str, &str, &str)],
    target_compositions: &CompositionTable,
) -> Vec<String> {
    let mut violations = Vec::new();
    for &(f, g, gf) in source_compositions {
        let Some(f_img) = functor.on_morphism(f) else {
            violations.push(format!("Composition law: F({}) is not defined", f));
            continue;
        };
        let Some(g_img) = functor.on_morphism(g) else {
            violations.push(format!("Composition law: F({}) is not defined", g));
            continue;
        };
        let Some(gf_img) = functor.on_morphism(gf) else {
            violations.push(format!("Composition law: F({}) is not defined", gf));
            continue;
        };

        let key = (f_img.to_string(), g_img.to_string());
        match target_compositions.get(&key) {
            Some(composed) if composed == gf_img => {}
            Some(composed) => {
                violations.push(format!(
                    "Composition law violated: F({}∘{}) = {} but F({})∘F({}) = {}",
                    g, f, gf_img, g, f, composed
                ));
            }
            None => {
                violations.push(format!(
                    "Composition law: F({})∘F({}) = {}∘{} not in target composition table",
                    g, f, g_img, f_img
                ));
            }
        }
    }
    violations
}

pub fn check_object_totality(
    functor: &DeclaredFiniteFunctor,
    source_objects: &[&str],
) -> Vec<String> {
    let mut violations = Vec::new();
    for &obj in source_objects {
        if functor.on_object(obj).is_none() {
            violations.push(format!(
                "Object totality: {} is not mapped by functor {}",
                obj, functor.name
            ));
        }
    }
    violations
}

pub fn check_morphism_totality(
    functor: &DeclaredFiniteFunctor,
    source_morphisms: &[&str],
) -> Vec<String> {
    let mut violations = Vec::new();
    for &mor in source_morphisms {
        if functor.on_morphism(mor).is_none() {
            violations.push(format!(
                "Morphism totality: {} is not mapped by functor {}",
                mor, functor.name
            ));
        }
    }
    violations
}

pub fn check_boundary_preservation(
    functor: &DeclaredFiniteFunctor,
    source_boundaries: &[(&str, &str, &str)],
    target_boundaries: &BTreeMap<String, (String, String)>,
) -> Vec<String> {
    let mut violations = Vec::new();

    for &(mor, src_obj, tgt_obj) in source_boundaries {
        let Some(f_img) = functor.on_morphism(mor) else {
            violations.push(format!("Boundary preservation: F({}) is not defined", mor));
            continue;
        };

        let Some(src_img) = functor.on_object(src_obj) else {
            violations.push(format!(
                "Boundary preservation: F({}) is not defined",
                src_obj
            ));
            continue;
        };

        let Some(tgt_img) = functor.on_object(tgt_obj) else {
            violations.push(format!(
                "Boundary preservation: F({}) is not defined",
                tgt_obj
            ));
            continue;
        };

        let Some((actual_src, actual_tgt)) = target_boundaries.get(f_img) else {
            violations.push(format!(
                "Boundary preservation: target boundary for F({}) = {} is not defined",
                mor, f_img
            ));
            continue;
        };

        if actual_src != src_img {
            violations.push(format!(
                "Boundary preservation violated for {}: src(F({})) = {}, expected F(src({})) = {}",
                mor, mor, actual_src, mor, src_img
            ));
        }

        if actual_tgt != tgt_img {
            violations.push(format!(
                "Boundary preservation violated for {}: tgt(F({})) = {}, expected F(tgt({})) = {}",
                mor, mor, actual_tgt, mor, tgt_img
            ));
        }
    }

    violations
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn declared_finite_functor_identity_law() {
        let mut f = DeclaredFiniteFunctor::new("Id", "C", "C");
        f.map_object("A", "A");
        f.map_object("B", "B");
        f.map_morphism("id_A", "id_A");
        f.map_morphism("id_B", "id_B");

        let violations = check_identity_law(&f);
        assert!(
            violations.is_empty(),
            "Identity law should pass: {:?}",
            violations
        );
    }

    #[test]
    fn declared_finite_functor_missing_mapping_is_violation() {
        let mut f = DeclaredFiniteFunctor::new("F", "C", "D");
        f.map_object("A", "X");
        let violations = check_identity_law(&f);
        assert_eq!(violations.len(), 1);
        assert!(violations[0].contains("not defined"));
    }

    #[test]
    fn composition_law_missing_mapping_is_violation() {
        let mut f = DeclaredFiniteFunctor::new("F", "C", "D");
        f.map_morphism("f", "Ff");
        f.map_morphism("gf", "Fgf");

        let target_comp: BTreeMap<(String, String), String> = BTreeMap::new();
        let violations = check_composition_law(&f, &[("f", "g", "gf")], &target_comp);
        assert!(!violations.is_empty());
        assert!(violations[0].contains("not defined"));
    }

    #[test]
    fn object_totality_check() {
        let mut f = DeclaredFiniteFunctor::new("F", "C", "D");
        f.map_object("A", "X");
        let violations = check_object_totality(&f, &["A", "B"]);
        assert_eq!(violations.len(), 1);
        assert!(violations[0].contains("B"));
    }
}
