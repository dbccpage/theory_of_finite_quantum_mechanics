//! Higher Inductive Types (HIT) module for homotopy type theory.
//!
//! Provides finite records for 0-cell point constructors, 1-cell path constructors,
//! and higher surface constructors, formalizing types like S^1, Interval, and Q^1 quotient HITs.

use crate::truncation::TruncationLevel;
use serde::{Deserialize, Serialize};

/// Point constructor (0-cell generator).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PointConstructor {
    pub name: String,
    pub doc: String,
}

/// Path constructor (1-cell generator equality between points).
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct PathConstructor {
    pub name: String,
    pub source_point: String,
    pub target_point: String,
    pub dimension: usize,
}

/// Higher Inductive Type specification.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct HigherInductiveType {
    pub type_name: String,
    pub points: Vec<PointConstructor>,
    pub paths: Vec<PathConstructor>,
    pub truncation_level: TruncationLevel,
}

impl HigherInductiveType {
    /// Construct a simple circle S^1 (base point + loop path).
    pub fn circle_s1() -> Self {
        Self {
            type_name: "S^1".to_string(),
            points: vec![PointConstructor {
                name: "base".to_string(),
                doc: "Base point of S1".to_string(),
            }],
            paths: vec![PathConstructor {
                name: "loop".to_string(),
                source_point: "base".to_string(),
                target_point: "base".to_string(),
                dimension: 1,
            }],
            truncation_level: TruncationLevel::Untruncated,
        }
    }

    /// Construct an Interval type I (left + right + seg).
    pub fn interval_i() -> Self {
        Self {
            type_name: "Interval".to_string(),
            points: vec![
                PointConstructor {
                    name: "left".to_string(),
                    doc: "Left endpoint 0".to_string(),
                },
                PointConstructor {
                    name: "right".to_string(),
                    doc: "Right endpoint 1".to_string(),
                },
            ],
            paths: vec![PathConstructor {
                name: "seg".to_string(),
                source_point: "left".to_string(),
                target_point: "right".to_string(),
                dimension: 1,
            }],
            truncation_level: TruncationLevel::Contractible,
        }
    }

    /// Check if the HIT definition has valid endpoint references.
    pub fn is_well_formed(&self) -> bool {
        let point_names: Vec<&str> = self.points.iter().map(|p| p.name.as_str()).collect();
        self.paths.iter().all(|path| {
            point_names.contains(&path.source_point.as_str())
                && point_names.contains(&path.target_point.as_str())
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_circle_well_formed() {
        let s1 = HigherInductiveType::circle_s1();
        assert!(s1.is_well_formed());
        assert_eq!(s1.points.len(), 1);
        assert_eq!(s1.paths.len(), 1);
    }

    #[test]
    fn test_interval_well_formed() {
        let interval = HigherInductiveType::interval_i();
        assert!(interval.is_well_formed());
        assert_eq!(interval.points.len(), 2);
        assert_eq!(interval.paths.len(), 1);
    }
}
