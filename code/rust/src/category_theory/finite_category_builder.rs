//! Ergonomic builder for declared finite categories.

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
        let morphisms = self
            .category
            .morphisms
            .values()
            .cloned()
            .collect::<Vec<_>>();

        for morphism in morphisms {
            if let Some(source_id) = self
                .category
                .identity_of(&morphism.source)
                .map(|identity| identity.to_string())
            {
                self.category
                    .set_composition(&source_id, &morphism.name, &morphism.name);
            }
            if let Some(target_id) = self
                .category
                .identity_of(&morphism.target)
                .map(|identity| identity.to_string())
            {
                self.category
                    .set_composition(&morphism.name, &target_id, &morphism.name);
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
