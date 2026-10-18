
use std::collections::BTreeMap;

use omega_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

use crate::derived::ChainComplex;
use crate::error::HigherCategoryError;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum ResolutionStrategy {
    Projective,
    Injective,
    KProjective,
    KInjective,
    Flat,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ChainComplexChain {
    pub id: String,
    pub stages: BTreeMap<i32, ChainComplex>,
    pub transition_maps: BTreeMap<i32, String>,
}

impl ChainComplexChain {
    pub fn new(id: &str) -> Self {
        Self {
            id: id.to_string(),
            stages: BTreeMap::new(),
            transition_maps: BTreeMap::new(),
        }
    }

    pub fn add_stage(&mut self, stage: i32, complex: ChainComplex) {
        self.stages.insert(stage, complex);
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct UnboundedDerivedCategory {
    pub name: String,
    pub complexes: BTreeMap<String, ChainComplex>,
    pub chains: BTreeMap<String, ChainComplexChain>,
    pub limits: OperationLimits,
}

impl UnboundedDerivedCategory {
    pub fn new(name: &str) -> Self {
        Self::with_limits(name, OperationLimits::default())
    }

    pub fn with_limits(name: &str, limits: OperationLimits) -> Self {
        Self {
            name: name.to_string(),
            complexes: BTreeMap::new(),
            chains: BTreeMap::new(),
            limits,
        }
    }

    pub fn add_complex(&mut self, complex: ChainComplex) -> Result<(), HigherCategoryError> {
        if self.complexes.contains_key(&complex.id) {
            return Err(HigherCategoryError::DuplicateCell { id: complex.id });
        }
        if self.complexes.len() >= self.limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: self.complexes.len() + 1,
                limit: self.limits.max_cells,
            });
        }
        complex.check_nilpotence()?;
        self.complexes.insert(complex.id.clone(), complex);
        Ok(())
    }

    pub fn add_chain(&mut self, chain: ChainComplexChain) -> Result<(), HigherCategoryError> {
        if self.chains.contains_key(&chain.id) {
            return Err(HigherCategoryError::DuplicateCell { id: chain.id });
        }
        if self.chains.len() >= self.limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: self.chains.len() + 1,
                limit: self.limits.max_cells,
            });
        }
        self.chains.insert(chain.id.clone(), chain);
        Ok(())
    }

    pub fn resolve(
        &self,
        complex_id: &str,
        strategy: ResolutionStrategy,
    ) -> Result<ChainComplex, HigherCategoryError> {
        let original = self
            .complexes
            .get(complex_id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound {
                id: complex_id.to_string(),
            })?;

        let resolved_id = format!("{strategy:?}({complex_id})");
        let mut resolved = ChainComplex::new(&resolved_id);

        for (&deg, gens) in &original.components {
            for g in gens {
                resolved.add_generator(deg, g);
                let diffs = original.differential_of(deg, g);
                resolved.set_differential(deg, g, diffs);
            }
        }

        resolved.check_nilpotence()?;
        Ok(resolved)
    }

    pub fn content_hash(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(self.name.as_bytes());
        for (id, comp) in &self.complexes {
            hasher.update(id.as_bytes());
            for (deg, gens) in &comp.components {
                hasher.update(&deg.to_be_bytes());
                for g in gens {
                    hasher.update(g.as_bytes());
                }
            }
        }
        format!("{:x}", hasher.finalize())
    }
}
