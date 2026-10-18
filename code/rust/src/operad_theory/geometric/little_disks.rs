//! Geometric: Little n-Disks Operad D_n.
//!
//! AuthorityEffect: None.

use serde::{Deserialize, Serialize};

/// A rectilinear disk embedding in R^n given by center and radius.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct RectilinearDisk {
    pub dimension: usize,
    pub center: Vec<f64>,
    pub radius: f64,
}

impl RectilinearDisk {
    pub fn new(dimension: usize, center: Vec<f64>, radius: f64) -> Result<Self, String> {
        if radius <= 0.0 {
            return Err(format!("Disk radius must be positive, got {}", radius));
        }
        if center.len() != dimension {
            return Err(format!("Center dimension {} != disk dimension {}", center.len(), dimension));
        }
        Ok(Self {
            dimension,
            center,
            radius,
        })
    }

    pub fn center_norm(&self) -> f64 {
        self.center.iter().map(|x| x * x).sum::<f64>().sqrt()
    }

    pub fn is_contained_in_unit_disk(&self) -> bool {
        self.center_norm() + self.radius <= 1.0 + 1e-9
    }

    pub fn is_disjoint_from(&self, other: &RectilinearDisk) -> Result<bool, String> {
        if self.dimension != other.dimension {
            return Err("Cannot check disjointness for disks of differing dimensions".to_string());
        }
        let dist = self
            .center
            .iter()
            .zip(&other.center)
            .map(|(a, b)| (a - b) * (a - b))
            .sum::<f64>()
            .sqrt();
        Ok(dist + 1e-9 >= self.radius + other.radius)
    }
}

/// A valid point in the topological operad space D_n(k).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct LittleDisksConfiguration {
    pub dimension: usize,
    pub disks: Vec<RectilinearDisk>,
}

impl LittleDisksConfiguration {
    pub fn new(dimension: usize, disks: Vec<RectilinearDisk>) -> Result<Self, String> {
        for d in &disks {
            if !d.is_contained_in_unit_disk() {
                return Err("Disk exceeds unit bounding ball".to_string());
            }
        }
        let n = disks.len();
        for i in 0..n {
            for j in (i + 1)..n {
                if !disks[i].is_disjoint_from(&disks[j])? {
                    return Err(format!("Disks at index {} and {} overlap in interior", i, j));
                }
            }
        }
        Ok(Self { dimension, disks })
    }

    pub fn arity(&self) -> usize {
        self.disks.len()
    }
}
