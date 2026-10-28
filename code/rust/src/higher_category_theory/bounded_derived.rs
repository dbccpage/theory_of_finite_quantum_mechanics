
use std::collections::BTreeMap;

use engine_kernel::resource_limits::OperationLimits;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

use crate::derived::ChainComplex;
use crate::error::HigherCategoryError;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct BoundedComplex {
    pub complex: ChainComplex,
    pub lower_bound: i32,
    pub upper_bound: i32,
}

impl BoundedComplex {
    pub fn new(complex: ChainComplex, lower: i32, upper: i32) -> Result<Self, HigherCategoryError> {
        if lower > upper {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: format!("lower bound <= upper bound, got {lower} > {upper}"),
                found: format!("lower={lower}, upper={upper}"),
            });
        }
        CohomologyBoundValidator::validate(&complex, lower, upper)?;
        Ok(Self {
            complex,
            lower_bound: lower,
            upper_bound: upper,
        })
    }
}

pub struct CohomologyBoundValidator;

impl CohomologyBoundValidator {
    pub fn validate(
        complex: &ChainComplex,
        lower: i32,
        upper: i32,
    ) -> Result<(), HigherCategoryError> {
        if lower > upper {
            return Err(HigherCategoryError::BoundaryMismatch {
                expected: format!("lower <= upper"),
                found: format!("{lower} > {upper}"),
            });
        }
        complex.check_nilpotence()?;

        for &deg in complex.components.keys() {
            if deg < lower || deg > upper {
                return Err(HigherCategoryError::BoundaryMismatch {
                    expected: format!("degree in bounded range [{lower}, {upper}]"),
                    found: format!("degree {deg}"),
                });
            }
        }
        Ok(())
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct BoundedDerivedCategory {
    pub name: String,
    pub complexes: BTreeMap<String, BoundedComplex>,
    pub limits: OperationLimits,
}

impl BoundedDerivedCategory {
    pub fn new(name: &str) -> Self {
        Self::with_limits(name, OperationLimits::default())
    }

    pub fn with_limits(name: &str, limits: OperationLimits) -> Self {
        Self {
            name: name.to_string(),
            complexes: BTreeMap::new(),
            limits,
        }
    }

    pub fn add_bounded_complex(
        &mut self,
        bounded: BoundedComplex,
    ) -> Result<(), HigherCategoryError> {
        if self.complexes.contains_key(&bounded.complex.id) {
            return Err(HigherCategoryError::DuplicateCell {
                id: bounded.complex.id,
            });
        }
        if self.complexes.len() >= self.limits.max_cells {
            return Err(HigherCategoryError::AllocationLimitExceeded {
                requested: self.complexes.len() + 1,
                limit: self.limits.max_cells,
            });
        }
        self.complexes.insert(bounded.complex.id.clone(), bounded);
        Ok(())
    }

    pub fn truncate_above(
        &self,
        id: &str,
        n: i32,
    ) -> Result<BoundedComplex, HigherCategoryError> {
        let original = self
            .complexes
            .get(id)
            .ok_or_else(|| HigherCategoryError::OneCellNotFound { id: id.to_string() })?;

        let trunc_id = format!("tau_le_{n}({})", original.complex.id);
        let mut new_comp = ChainComplex::new(&trunc_id);

        for (&deg, gens) in &original.complex.components {
            if deg <= n {
                for g in gens {
                    new_comp.add_generator(deg, g);
                    let diffs = original.complex.differential_of(deg, g);
                    let filtered_diffs: Vec<(i64, String)> = diffs
                        .into_iter()
                        .filter(|(_c, _target)| {
                            deg - 1 <= n
                        })
                        .collect();
                    new_comp.set_differential(deg, g, filtered_diffs);
                }
            }
        }

        let new_lower = original.lower_bound.min(n);
        let new_upper = original.upper_bound.min(n);
        BoundedComplex::new(new_comp, new_lower, new_upper)
    }

    pub fn content_hash(&self) -> String {
        let mut hasher = Sha256::new();
        hasher.update(self.name.as_bytes());
        for (id, bc) in &self.complexes {
            hasher.update(id.as_bytes());
            hasher.update(&bc.lower_bound.to_be_bytes());
            hasher.update(&bc.upper_bound.to_be_bytes());
        }
        format!("{:x}", hasher.finalize())
    }
}
