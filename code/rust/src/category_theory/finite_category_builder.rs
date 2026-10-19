//! Fluent raw finite-category declarations. AuthorityEffect: None.
//!
//! Mutators may overwrite existing names and table entries. Generated `id_`
//! names are a recipe, not fresh-name guarantees. `identity_checked` checks
//! only a loop boundary; `build_validated` separately performs full admission.

use super::finite_category::{DeclaredFiniteCategory, ValidatedFiniteCategory};
use super::validation::ValidationReport;

#[derive(Debug, Clone)]
pub struct DeclaredFiniteCategoryBuilder {
    category: DeclaredFiniteCategory,
}

impl DeclaredFiniteCategoryBuilder {
    pub fn new(name: &str) -> Self {
        Self {
            category: DeclaredFiniteCategory::new(name),
        }
    }

    pub fn walking_arrow(name: &str, source: &str, target: &str, arrow: &str) -> Self {
        Self::new(name)
            .identity_object(source)
            .identity_object(target)
            .morphism(arrow, source, target)
            .identity_compositions()
    }

    pub fn object(mut self, object: &str) -> Self {
        self.category.add_object(object);
        self
    }

    pub fn morphism(mut self, name: &str, source: &str, target: &str) -> Self {
        self.category.add_morphism(name, source, target);
        self
    }

    pub fn identity(mut self, object: &str, morphism: &str) -> Self {
        self.category.add_identity(object, morphism);
        self
    }

    pub fn identity_checked(mut self, object: &str, morphism: &str) -> Result<Self, String> {
        if let Some((src, tgt)) = self.category.boundary_of(morphism) {
            if src != object || tgt != object {
                return Err(format!(
                    "Cannot set {} as identity of {}: boundary is {} → {}",
                    morphism, object, src, tgt
                ));
            }
        } else {
            self.category.add_morphism(morphism, object, object);
        }

        self.category.set_identity(object, morphism);
        Ok(self)
    }

    pub fn identity_object(mut self, object: &str) -> Self {
        let id = format!("id_{}", object);
        self.category.add_morphism(&id, object, object);
        self.category.set_identity(object, &id);
        self
    }

    /// Adds composition second ∘ first = composite.
    pub fn composition(mut self, first: &str, second: &str, composite: &str) -> Self {
        self.category.set_composition(first, second, composite);
        self
    }

    /// Alias for `composition`, emphasizing that `(f, g)` means `g` after `f`.
    pub fn path_composition(mut self, f: &str, g: &str, composite: &str) -> Self {
        self.category.set_composition(f, g, composite);
        self
    }

    /// Adds the identity compositions forced by the currently declared
    /// identities and morphism boundaries.
    pub fn identity_compositions(mut self) -> Self {
        let DeclaredFiniteCategory {
            morphisms,
            identities,
            compositions,
            ..
        } = &mut self.category;
        // Borrow separate maps; only owned table keys/new values need copies.
        for morphism in morphisms.values() {
            if let Some(source_id) = identities.get(&morphism.source) {
                compositions
                    .entry((source_id.clone(), morphism.name.clone()))
                    .and_modify(|value| value.clone_from(&morphism.name))
                    .or_insert_with(|| morphism.name.clone());
            }
            if let Some(target_id) = identities.get(&morphism.target) {
                compositions
                    .entry((morphism.name.clone(), target_id.clone()))
                    .and_modify(|value| value.clone_from(&morphism.name))
                    .or_insert_with(|| morphism.name.clone());
            }
        }

        self
    }

    pub fn build(self) -> DeclaredFiniteCategory {
        self.category
    }

    pub fn build_validated(self) -> Result<ValidatedFiniteCategory, ValidationReport> {
        ValidatedFiniteCategory::try_new(self.category)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn builder_can_validate_walking_arrow() {
        let category = DeclaredFiniteCategoryBuilder::walking_arrow("WalkingArrow", "A", "B", "f")
            .build_validated();

        assert!(category.is_ok());
    }
}
