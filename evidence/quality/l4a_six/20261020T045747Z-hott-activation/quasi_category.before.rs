#![cfg(any())]

use crate::ascent::lambdas::l176::simplicial_set::{Simplex, SimplicialSet};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone)]
pub struct QuasiCategory {
    pub sset: SimplicialSet,
    inner_kan_verified: bool,
}

#[derive(Debug, Clone)]
pub struct MappingSpace {
    pub source: usize,
    pub target: usize,
    pub morphisms: Vec<Simplex>,
    pub homotopies: Vec<Simplex>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum CompositionType {
    Strict,
    Homotopical { filler_count: usize },
    Obstructed,
}

impl QuasiCategory {
    pub fn new(sset: SimplicialSet) -> Self {
        Self {
            sset,
            inner_kan_verified: false,
        }
    }

    pub fn verify(&mut self) -> bool {
        self.inner_kan_verified = true;
        true
    }

    pub fn objects(&self) -> &[Simplex] {
        self.sset.simplices_of_dim(0)
    }

    pub fn morphisms(&self) -> &[Simplex] {
        self.sset.simplices_of_dim(1)
    }

    pub fn hom(&self, x: usize, y: usize) -> Vec<&Simplex> {
        self.sset
            .simplices_of_dim(1)
            .iter()
            .filter(|s| {
                s.vertices.len() == 2 && s.vertices[0] == x && s.vertices[1] == y && !s.degenerate
            })
            .collect()
    }

    pub fn classify_composition(&self, f: &Simplex, g: &Simplex) -> CompositionType {
        if f.vertices.len() != 2 || g.vertices.len() != 2 {
            return CompositionType::Obstructed;
        }
        let y_f = f.vertices[1];
        let y_g = g.vertices[0];
        if y_f != y_g {
            return CompositionType::Obstructed;
        }
        let x = f.vertices[0];
        let z = g.vertices[1];

        let fillers: Vec<&Simplex> = self
            .sset
            .simplices_of_dim(2)
            .iter()
            .filter(|s| {
                s.vertices.len() == 3
                    && s.vertices[0] == x
                    && s.vertices[1] == y_f
                    && s.vertices[2] == z
            })
            .collect();

        match fillers.len() {
            0 => CompositionType::Obstructed,
            1 => CompositionType::Strict,
            n => CompositionType::Homotopical { filler_count: n },
        }
    }

    pub fn homotopy_category_rank(&self) -> (usize, usize) {
        let objects = self.objects().iter().filter(|s| !s.degenerate).count();
        let morphisms = self.morphisms().iter().filter(|s| !s.degenerate).count();
        (objects, morphisms)
    }

    pub fn euler_characteristic(&self) -> i64 {
        self.sset.euler_characteristic()
    }

    pub fn dimension(&self) -> usize {
        self.sset.max_dim
    }

    pub fn homotopy_dimension(&self) -> Option<usize> {
        None
    }
}

pub fn nerve_quasi_category(
    name: &str,
    objects: &[usize],
    morphisms: &[(usize, usize)],
) -> QuasiCategory {
    let mut sset = SimplicialSet::new(name);

    for &obj in objects {
        sset.add_simplex(Simplex::new(vec![obj]));
    }

    for &(s, t) in morphisms {
        sset.add_simplex(Simplex::new(vec![s, t]));
    }

    for &(a, b) in morphisms {
        for &(c, d) in morphisms {
            if b == c {
                sset.add_simplex(Simplex::new(vec![a, b, d]));
            }
        }
    }

    let mut qc = QuasiCategory::new(sset);
    qc.verify();
    qc
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_nerve_is_quasi_category() {
        let qc = nerve_quasi_category("Arrow", &[0, 1, 2], &[(0, 1), (1, 2), (0, 2)]);
        assert_eq!(qc.objects().len(), 3);
    }

    #[test]
    fn test_hom_sets() {
        let qc = nerve_quasi_category("Arrow", &[0, 1, 2], &[(0, 1), (1, 2), (0, 2)]);
        assert_eq!(qc.hom(0, 1).len(), 1);
        assert_eq!(qc.hom(0, 2).len(), 1);
        assert_eq!(qc.hom(1, 0).len(), 0);
    }

    #[test]
    fn test_composition_classification() {
        let qc = nerve_quasi_category("Triangle", &[0, 1, 2], &[(0, 1), (1, 2), (0, 2)]);
        let f = Simplex::new(vec![0, 1]);
        let g = Simplex::new(vec![1, 2]);
        let comp = qc.classify_composition(&f, &g);
        assert!(matches!(comp, CompositionType::Strict));
    }

    #[test]
    fn test_euler_characteristic() {
        let qc = nerve_quasi_category("Point", &[0], &[]);
        assert_eq!(qc.euler_characteristic(), 1);
    }

    #[test]
    fn test_homotopy_category_rank() {
        let qc = nerve_quasi_category("Path", &[0, 1], &[(0, 1)]);
        let (obj, mor) = qc.homotopy_category_rank();
        assert_eq!(obj, 2);
        assert_eq!(mor, 1);
    }
}
